import datetime
from functools import reduce
from decimal import Decimal

from django.db import (models as django_models, DatabaseError, transaction)
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_delete

from django.contrib.auth.models import AbstractUser
from django.conf import settings

from i18nfield.fields import I18nCharField, I18nTextField

from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet

from djmoney.money import Money
from djmoney.contrib.exchange.models import convert_money

from .exceptions import (NoEnoughQuotaException,
                         NonFinishedUserReservationsException,
                         NonUpdatableReservationException,
                         NonReviewableReservation)
from .utils import file_cleanup


class ReservationQuerySet(django_models.QuerySet):
    def update_expired_reservations(self):
        # We give the student one more day to upload his receipt

        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        expired_reservations = self.filter(status__in=Reservation.EXPIRABLE_STATUS_LIST,
                                           confirmation_deadline_date__lt=yesterday)
        result = expired_reservations.count()

        expired_reservations.update(status=Reservation.EXPIRED_STATUS,
                                    last_update_date=datetime.date.today())

        return result

    def status_statistics(self):
        self.update_expired_reservations()

        def count_status(status):
            return django_models.Count('status', filter=django_models.Q(
                status=status))

        result = self.aggregate(
            pending_reservations=count_status(Reservation.PENDING_STATUS),
            rejected_reservations=count_status(Reservation.REJECTED_STATUS),
            confirmed_reservations=count_status(Reservation.CONFIRMED_STATUS),
            waiting_for_manager_action_reservations=count_status(
                Reservation.WAITING_FOR_MANAGER_ACTION_STATUS),
            manager_updated_reservations=count_status(Reservation.MANAGER_UPDATED_STATUS),
            expired_reservations=count_status(Reservation.EXPIRED_STATUS))

        return result


class DormitoryQuerySet(django_models.QuerySet):
    def apply_room_filters(self, filters, to_currency=None):

        def get_prices_converted_cases(filtered_rooms):
            filtered_rooms_ids = filtered_rooms.values_list('id', flat=True)
            original_prices = IntegralChoice.objects.filter(
                related_filter__name__contains='Price', room_characteristics__id__in=filtered_rooms_ids).values_list('room_characteristics__id', 'selected_number')
            price_whens = [django_models.When(id=k, then=v) for k, v in original_prices]
            original_price_cases = django_models.Case(
                *price_whens, default=0, output_field=django_models.IntegerField())
            prices_to_convert = filtered_rooms.annotate(
                original_price=original_price_cases).values_list('id', 'original_price', 'price_currency__code')

            converted_prices = {}
            for id, original_price, from_currency in prices_to_convert:
                #print(id, original_price, from_currency)
                converted_prices[id] = int(convert_money(
                    Money(original_price, from_currency), to_currency).amount)

            whens = [django_models.When(id=k, then=v) for k, v in converted_prices.items()]
            new_prices_cases = django_models.Case(
                *whens, default=0, output_field=django_models.IntegerField())

            return new_prices_cases

        if not to_currency or not Currency.objects.filter(code=to_currency).exists():
            to_currency = 'USD'

        filtered_rooms = RoomCharacteristics.objects.filter(allowed_quota__gte=1)

        if filters:
            # print(filtered_rooms)

            for current_filter in filters:
                filtered_rooms = filtered_rooms.filter(current_filter)

            filtered_rooms = filtered_rooms.annotate(
                price_converted=get_prices_converted_cases(filtered_rooms))

            filtered_rooms.prefetch_related('features', 'radio_choices', 'integral_choices',
                                            'radio_choices__related_filter',
                                            'integral_choices__related_filter')

            room_characteristics = django_models.Prefetch(
                'room_characteristics', queryset=filtered_rooms)

            dorms = self.filter(room_characteristics__in=filtered_rooms)\
                        .prefetch_related(room_characteristics).distinct()

        else:
            filtered_rooms = filtered_rooms.annotate(
                price_converted=get_prices_converted_cases(filtered_rooms))

            room_characteristics = django_models.Prefetch(
                'room_characteristics', queryset=filtered_rooms)
            dorms = self.prefetch_related(room_characteristics).distinct()

        return dorms

    def apply_dorm_filters(self, filters):
        if filters:
            dorms = self.filter(filters[0])
            for current_filter in filters:
                dorms = dorms.filter(current_filter)

            # dorms.prefetch_related('features')
        else:
            dorms = self

        return dorms

    def available(self):
        return self.filter(room_characteristics__allowed_quota__gte=1)

    def with_last_3_reviews(self):
        last_3_reviews = django_models.Subquery(
            Review.objects.filter(dormitory__in=self,
                                  dormitory_id=django_models.OuterRef('dormitory_id')).values_list('id', flat=True)[:3])

        prefetch_reviews = django_models.Prefetch(
            'reviews', queryset=Review.objects.filter(id__in=last_3_reviews))
        return self.prefetch_related(prefetch_reviews)

    def with_reviews_statistics(self):
        reviews_count = django_models.Count('reviews', distinct=True)
        reviews_avg = django_models.Avg('reviews__stars', distinct=True)
        return self.annotate(number_of_reviews=reviews_count, stars_average=reviews_avg)

    def superfilter(self, category_id=None, duration_option_id=None,
                    dorm_features_ids=None, radio_integeral_choices=None, room_features_ids=None,
                    to_currency=None):

        result = self

        if category_id:
            result = result.filter(category__id=category_id)

        result = result.available()

        dorm_filters = []

        if dorm_features_ids:
            for current_feature_id in dorm_features_ids:
                current_filter = Filter.objects.filter(id=current_feature_id).first()
                dorm_filters.append(current_filter.get_query())

        room_filters = []

        if duration_option_id:
            duration_option = RadioOption.objects.filter(id=duration_option_id).first()
            duration_filter = duration_option.related_filter.get_query(duration_option_id)
            room_filters.append(duration_filter)

        if room_features_ids:
            for current_feature_id in room_features_ids:
                current_filter = Filter.objects.filter(id=current_feature_id).first()
                room_filters.append(current_filter.get_query())

        if radio_integeral_choices:
            non_empty_radio_integeral_choices = [
                x for x in radio_integeral_choices if x.get('choosen_options_ids', None) != []]

            for choice in non_empty_radio_integeral_choices:
                current_filter = Filter.objects.filter(id=choice['id']).first()
                room_filters.append(current_filter.get_query_polymorphic(choice))

        result = result.apply_dorm_filters(dorm_filters)\
                       .apply_room_filters(room_filters, to_currency)\
                       .annotate(rooms_left_in_dorm=django_models.Sum(
                           'room_characteristics__allowed_quota'))

        return result


class FilterQuerySet(PolymorphicQuerySet):

    def radio_filters(self):
        result = self.instance_of(RadioFilter).exclude(django_models.Q(name__contains='Duration'))
        return result

    def integral_filters(self):
        result = self.instance_of(IntegralFilter)
        return result

    def additional_filters(self):
        return (self.radio_filters() | self.integral_filters()).distinct()

    def dorm_features(self):
        return self.instance_of(FeatureFilter).filter(featurefilter__is_dorm_feature=True)

    def room_features(self):
        return self.instance_of(FeatureFilter).filter(featurefilter__is_dorm_feature=False)


class Filter(PolymorphicModel):
    name = I18nCharField(max_length=60)

    objects = PolymorphicManager.from_queryset(FilterQuerySet)()

    def __str__(self):
        return f'{self.name} filter'


class RadioFilter(Filter):
    is_optional = django_models.BooleanField(default=True)

    def get_query(self, selected_options):
        only_one_selected_option = isinstance(selected_options, int)
        if only_one_selected_option:
            selected_options = [selected_options]

        return (django_models.Q(radio_choices__related_filter__id=self.id) &
                django_models.Q(radio_choices__selected_option__id__in=selected_options))

    def get_query_polymorphic(self, json_choice):
        option_ids = json_choice['choosen_options_ids']
        return self.get_query(option_ids)

    def __str__(self):
        return f'{self.name} radio filter'


class IntegralFilter(Filter):
    is_optional = django_models.BooleanField(default=True)

    def get_query(self, min, max):
        return (django_models.Q(integral_choices__related_filter__id=self.id) &
                django_models.Q(integral_choices__selected_number__gte=min) &
                django_models.Q(integral_choices__selected_number__lte=max))

    def get_query_polymorphic(self, json_min_max):
        return self.get_query(json_min_max['min_value'], json_min_max['max_value'])

    def __str__(self):
        return f'{self.name} intgeral filter'


class FeatureFilter(Filter):
    icon = django_models.CharField(max_length=100)
    is_dorm_feature = django_models.BooleanField(default=False)

    def get_query(self):
        return django_models.Q(features__id=self.id)

    def __str__(self):
        return f'{self.name} filter'


class RadioOption(django_models.Model):
    name = I18nCharField(max_length=60)

    related_filter = django_models.ForeignKey(
        RadioFilter, related_name='options', on_delete=django_models.CASCADE)

    def __str__(self):
        return f'{self.name} option'


class Choice(PolymorphicModel):
    pass


class IntegralChoice(Choice):
    selected_number = django_models.PositiveIntegerField(default=0)

    related_filter = django_models.ForeignKey(
        IntegralFilter, related_name='integral_choices', on_delete=django_models.CASCADE)

    def __str__(self):
        return f'{self.related_filter.name} choice with number {self.selected_number}'


class RadioChoice(Choice):
    selected_option = django_models.ForeignKey(
        RadioOption, related_name='radio_choices', on_delete=django_models.CASCADE)
    related_filter = django_models.ForeignKey(
        RadioFilter, related_name='radio_choices', on_delete=django_models.CASCADE)

    def __str__(self):
        return f'{self.related_filter.name} choice with {self.selected_option}'


class Currency(django_models.Model):
    symbol = django_models.CharField(max_length=1)
    code = django_models.CharField(max_length=9)

    def __str__(self):
        return f'{self.code} Currency with Symbol {self.symbol}'

    class Meta:
        verbose_name_plural = 'Currencies'


class DormitoryCategory(django_models.Model):
    name = I18nCharField(max_length=60)

    class Meta:
        verbose_name_plural = 'Dormitory categories'


class User(AbstractUser):
    is_manager = django_models.BooleanField(default=False)


class Dormitory(django_models.Model):
    name = django_models.CharField(max_length=60)
    about = I18nTextField()

    geo_longitude = django_models.CharField(max_length=20)
    geo_latitude = django_models.CharField(max_length=20)
    address = django_models.CharField(max_length=150)

    contact_name = django_models.CharField(max_length=60)
    contact_email = django_models.CharField(max_length=60)
    contact_number = django_models.CharField(max_length=60)
    contact_fax = django_models.CharField(max_length=60)

    cover = django_models.ImageField()

    category = django_models.ForeignKey(
        DormitoryCategory, related_name='dormitories', on_delete=django_models.CASCADE)

    features = django_models.ManyToManyField(
        FeatureFilter, related_name='dormitories')

    manager = django_models.ForeignKey(
        User, related_name='dormitories', on_delete=django_models.CASCADE)

    objects = DormitoryQuerySet.as_manager()

    def is_owner(self, manager):
        return self.manager == manager

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Dormitories'


class BankAccount(django_models.Model):
    bank_name = django_models.CharField(max_length=60)

    account_name = django_models.CharField(max_length=60)
    account_number = django_models.CharField(max_length=60)

    iban = django_models.CharField(max_length=60)
    swift = django_models.CharField(max_length=60)

    currency = django_models.ForeignKey(
        Currency, related_name='bank_accounts', on_delete=django_models.CASCADE)

    dormitory = django_models.ForeignKey(
        Dormitory, related_name='bank_accounts', on_delete=django_models.CASCADE)

    def is_owner(self, manager):
        return self.dormitory.manager == manager

    def __str__(self):
        return f'BankAccount id {self.id} name {self.bank_name} in {self.dormitory.name}'


class RoomCharacteristics(django_models.Model):
    total_quota = django_models.PositiveIntegerField(default=0)
    allowed_quota = django_models.PositiveIntegerField(default=0)

    price_currency = django_models.ForeignKey(
        Currency, related_name='room_characteristics', on_delete=django_models.CASCADE)

    room_confirmation_days = django_models.PositiveIntegerField(default=2)

    radio_choices = django_models.ManyToManyField(
        RadioChoice, related_name='room_characteristics')

    integral_choices = django_models.ManyToManyField(
        IntegralChoice, related_name='room_characteristics')

    features = django_models.ManyToManyField(
        FeatureFilter, related_name='room_characteristics')

    dormitory = django_models.ForeignKey(
        Dormitory, related_name='room_characteristics', on_delete=django_models.CASCADE)

    @property
    def duration(self):
        return self.radio_choices.filter(related_filter__name__contains='Duration')\
            .first().selected_option.name

    @property
    def price(self):
        # maybe no price conversion required
        try:
            if self.price_converted:
                return self.price_converted
        except AttributeError:
            # we use contains as we have multiple langs names
            return self.integral_choices.filter(related_filter__name__contains='Price')\
                .first().selected_number

    @property
    def room_type(self):
        return self.radio_choices.filter(related_filter__name__contains='Room Type')\
            .first().selected_option.name

    @property
    def people_allowed_number(self):
        return self.integral_choices.filter(related_filter__name__contains='People Allowed Number')\
                                    .first().selected_number

    def increase_quota(self):
        self.allowed_quota += 1

    def decrease_quota(self):
        if self.allowed_quota == 0:
            raise NoEnoughQuotaException()

        self.allowed_quota -= 1

    def __str__(self):
        return f'Room id {self.id} in {self.dormitory.name}'

    class Meta:
        verbose_name_plural = 'Rooms'


class Reservation(django_models.Model):
    PENDING_STATUS = '0'
    REJECTED_STATUS = '1'
    CONFIRMED_STATUS = '2'
    WAITING_FOR_MANAGER_ACTION_STATUS = '3'
    MANAGER_UPDATED_STATUS = '4'
    EXPIRED_STATUS = '5'

    EXPIRABLE_STATUS_LIST = [PENDING_STATUS, MANAGER_UPDATED_STATUS]
    NON_UPDATABLE_STATUS_LIST = [REJECTED_STATUS, CONFIRMED_STATUS, EXPIRED_STATUS]

    STATUS_CHARS_LIST = [PENDING_STATUS, REJECTED_STATUS, CONFIRMED_STATUS,
                         WAITING_FOR_MANAGER_ACTION_STATUS, MANAGER_UPDATED_STATUS]

    STATUS_CHOICES = (
        (PENDING_STATUS, 'pending'),
        (REJECTED_STATUS, 'rejected'),
        (CONFIRMED_STATUS, 'confirmed'),
        (WAITING_FOR_MANAGER_ACTION_STATUS, 'waiting-manager-action'),
        (MANAGER_UPDATED_STATUS, 'manager-updated'),
        (EXPIRED_STATUS, 'expired-dont-choose-this'),
    )

    reservation_creation_date = django_models.DateField(auto_now=True)
    is_reviewed = django_models.BooleanField(default=False)

    status = django_models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=PENDING_STATUS)
    confirmation_deadline_date = django_models.DateField()

    last_update_date = django_models.DateField(blank=True, null=True)
    follow_up_message = django_models.CharField(max_length=300)

    user = django_models.ForeignKey(
        User, related_name='reservations', on_delete=django_models.CASCADE)

    room_characteristics = django_models.ForeignKey(
        RoomCharacteristics, related_name='reservations', on_delete=django_models.CASCADE)

    @property
    def is_past_confirmation_deadline(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        return self.confirmation_deadline_date < yesterday

    @property
    def is_reviewable(self):
        """The reservation becomes reviewable after three months"""
        if settings.IS_ALWAYS_REVIEWABLE:
            return True

        not_reviewed = self.is_reviewed == False
        confirmed = self.status == Reservation.CONFIRMED_STATUS
        if confirmed and not_reviewed:
            today_and_creation_date_difference = datetime.date.today() - self.reservation_creation_date
            result = today_and_creation_date_difference.days >= 90
            # print(today_and_creation_date_difference.days)
        else:
            result = False

        return result

    def is_owner(self, manager):
        return self.room_characteristics.dormitory.manager == manager

    objects = ReservationQuerySet.as_manager()

    class Meta:
        ordering = ['-reservation_creation_date']

    @classmethod
    def create(cls, *args, **kwargs):

        def cleanup_reservations(reservations, current_reserved_room):
            cleanup_operations = []
            reservations = reservations.all()
            for reservation in reservations:
                not_same_reserved_room = reservation.room_characteristics.id != current_reserved_room.id
                if not_same_reserved_room:
                    reservation.room_characteristics.increase_quota()
                    cleanup_operations.append(reservation.room_characteristics.save)

                cleanup_operations.append(reservation.delete)

            return cleanup_operations

        def throw_error_if_user_has_non_finished_reservations(user):
            non_finished_reservations_query = django_models.Q(
                status=Reservation.WAITING_FOR_MANAGER_ACTION_STATUS) | django_models.Q(
                status=Reservation.MANAGER_UPDATED_STATUS)

            user_non_finished_reservations = user.reservations.filter(
                non_finished_reservations_query).count()

            if user_non_finished_reservations > 0:
                raise NonFinishedUserReservationsException()

        room_characteristics = kwargs['room_characteristics']
        user = kwargs['user']

        throw_error_if_user_has_non_finished_reservations(user)

        user_pending_reservations = user.reservations.filter(
            status=Reservation.PENDING_STATUS)

        confirmation_deadline_date = datetime.date.today() + datetime.timedelta(
            days=room_characteristics.room_confirmation_days)
        result = cls(confirmation_deadline_date=confirmation_deadline_date, *args, **kwargs)

        with transaction.atomic():
            not_same_room = user_pending_reservations.filter(
                room_characteristics_id=room_characteristics.id).exists() == False
            if not_same_room:
                room_characteristics.decrease_quota()
            #print('qooq', room_characteristics.allowed_quota)

            cleanup_operations = cleanup_reservations(
                user_pending_reservations, room_characteristics)

            result.save()
            room_characteristics.save()
            for operation in cleanup_operations:
                operation()

        return result

    def update_status(self, new_status):
        self.status = new_status
        self.last_update_date = datetime.date.today()

        if new_status == Reservation.REJECTED_STATUS or new_status == Reservation.EXPIRED_STATUS:
            self.room_characteristics.increase_quota()
            with transaction.atomic():
                self.save()
                self.room_characteristics.save()

    def check_if_expired(self):
        if self.is_past_confirmation_deadline:
            self.update_status(Reservation.EXPIRED_STATUS)
        return self

    def add_receipt(self, receipt):
        if self.status in Reservation.NON_UPDATABLE_STATUS_LIST:
            raise NonUpdatableReservationException()

        self.status = Reservation.WAITING_FOR_MANAGER_ACTION_STATUS

        with transaction.atomic():
            receipt.save()
            self.save()

    def create_review(self, *args, **kwargs):
        if not self.is_reviewable:
            raise NonReviewableReservation()

        review = Review(
            user=self.user, dormitory=self.room_characteristics.dormitory, *args, **kwargs)

        self.is_reviewed = True

        with transaction.atomic():
            self.save()
            review.save()

    def is_owner(self, user):
        return self.user == user

    def __str__(self):
        return f'Reservation id {self.id} status {self.status} for {self.user} {self.room_characteristics}'


class Review(django_models.Model):
    review_creation_date = django_models.DateField(auto_now=True)
    stars = django_models.DecimalField(decimal_places=1, max_digits=2,
                                       validators=[MinValueValidator(Decimal('0.0')),
                                                   MaxValueValidator(Decimal('5.0'))])
    description = django_models.TextField()

    user = django_models.ForeignKey(
        User, related_name='reviews', on_delete=django_models.CASCADE)
    dormitory = django_models.ForeignKey(
        Dormitory, related_name='reviews', on_delete=django_models.CASCADE)

    class Meta:
        ordering = ['-review_creation_date']

    def __str__(self):
        return f'Review id {self.id} for {self.user}'


class UploadablePhoto(django_models.Model):
    photo = django_models.ImageField(upload_to='')

    @property
    def url(self):
        if self.is_3d:
            return self.photo.url.replace('/media/', '')
        else:
            return self.photo.path

    class Meta:
        abstract = True


class RoomPhoto(UploadablePhoto):
    is_3d = django_models.BooleanField(default=False)

    room_characteristics = django_models.ForeignKey(
        RoomCharacteristics, related_name='photos', on_delete=django_models.CASCADE)


post_delete.connect(file_cleanup, sender=RoomPhoto, dispatch_uid="gallery.image.file_cleanup")


class DormitoryPhoto(UploadablePhoto):
    is_3d = django_models.BooleanField(default=False)

    dormitory = django_models.ForeignKey(
        Dormitory, related_name='photos', on_delete=django_models.CASCADE)

    def is_owner(self, manager):
        return self.dormitory.manager == manager


post_delete.connect(file_cleanup, sender=DormitoryPhoto, dispatch_uid="gallery.image.file_cleanup")


class ReceiptPhoto(UploadablePhoto):
    upload_receipt_date = django_models.DateField(auto_now=True)

    @property
    def url(self):
        return self.photo.path

    reservation = django_models.ForeignKey(
        Reservation, related_name='receipts', on_delete=django_models.CASCADE)


post_delete.connect(file_cleanup, sender=ReceiptPhoto, dispatch_uid="gallery.image.file_cleanup")
