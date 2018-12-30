import datetime

from django.db import models as django_models
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from rest_framework import serializers

from allauth.account.forms import ResetPasswordForm, default_token_generator, UserTokenForm
from allauth.account.adapter import get_adapter
from allauth.account.utils import send_email_confirmation, user_pk_to_url_str, setup_user_email
from allauth.account import app_settings as allauth_settings


from allauth.utils import email_address_exists

from i18nfield.rest_framework import I18nField

from rest_polymorphic.serializers import PolymorphicSerializer

from .utils import i18n

from . import models


class LocalRemoteURLField(serializers.URLField):
    def to_representation(self, value):
        result = super().to_representation(value)
        if not settings.IS_PRODUCTION:
            result = result[result.find(r'\media'):]
        return result


class PhotoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    url = LocalRemoteURLField()
    is_3d = serializers.BooleanField(default=False)

    class Meta:
        fields = ('id', 'url', 'is_3d')


class ReviewSerializer(serializers.ModelSerializer):
    review_creation_date = serializers.DateField(read_only=True, format = '%Y-%m-%d')
    stars = serializers.DecimalField(decimal_places=1, max_digits=2)
    description = serializers.CharField(required=False)
    student_name = serializers.CharField(read_only=True, source='user.first_name')

    def save(self, *args, **kwargs):
        #print('qoooq', self.context.get('reservation_id'))
        reservation = models.Reservation.objects.get(pk=self.context.get('reservation_id'))
        #print(**self.validated_data)
        reservation.create_review(**self.validated_data)
        

    class Meta:
        model = models.Review
        fields = ('review_creation_date', 'stars',
                  'description', 'student_name')

class AskForReviewSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()

    def save(self, *args, **kwargs):
        request = self.context.get('request')

        current_site = get_current_site(request)
        reservation_id = self.validated_data['reservation_id']

        reservation = models.Reservation.objects.get(pk=reservation_id)
        if not reservation.is_reviewable:
            raise serializers.ValidationError(i18n.t('student.errorMessages.manageReservation.thisReservationIsNotReviewable'))

        user = reservation.user

        path = f'/reservations/{reservation_id}/review'
        url = settings.BASE_URL + path
        context = {'current_site': current_site,
                   'user': user,
                   'review_url': url,
                   'request': request}

        get_adapter().send_mail(
            'review/email/ask_for_review',
            user.email,
            context)

    class Meta:
        fields = ('reservation_id', )


class UserSerializer(serializers.ModelSerializer):
    EMAIL_CONFIRMED = 2
    NON_PENDING_RESERVATION = 3

    name = serializers.CharField(source='first_name')
    email = serializers.CharField()
    is_manager = serializers.BooleanField(read_only=True)
    reservation_id = serializers.SerializerMethodField()
    current_step = serializers.SerializerMethodField()

    def get_reservation_id(self, obj):
        self._reservation = obj.reservations.first()
        if self._reservation:
            result = self._reservation.id
        else:
            result = None

        return result

    def get_current_step(self, obj):
        result = UserSerializer.EMAIL_CONFIRMED
        if self._reservation:
            status = self._reservation.status
            if status != models.Reservation.PENDING_STATUS:
                result = UserSerializer.NON_PENDING_RESERVATION

        return result

    class Meta:
        model = models.User
        fields = ('name', 'email', 'is_manager',
                  'reservation_id', 'current_step')

class BankAccountSerializer(serializers.ModelSerializer):
    currency_code=serializers.CharField(source='currency.code')

    class Meta:
        model=models.BankAccount
        fields=('id', 'bank_name', 'account_name',
                  'account_number', 'swift', 'iban', 'currency_code')

class ReservationDormitorySerializer(serializers.ModelSerializer):
    bank_accounts=BankAccountSerializer(many = True)

    class Meta:
        model=models.Dormitory
        fields=('id',
                  'contact_name', 'contact_email', 'contact_number', 'contact_fax',
                  'bank_accounts')

class ReceiptSerializer(serializers.ModelSerializer):
    url=LocalRemoteURLField(read_only = True)
    upload_receipt_date=serializers.DateField(format = '%Y-%m-%d', required = False, read_only = True)
    uploaded_photo=serializers.ImageField(required = False)

    def create(self, validated_data):
        uploaded_photo=validated_data.get('uploaded_photo', None)
        reservation=models.Reservation.objects.get(pk = self.context['reservation_pk'])

        instance=models.ReceiptPhoto(photo = uploaded_photo, reservation = reservation)

        reservation.add_receipt(instance)

        return instance

    class Meta:
        model=models.ReceiptPhoto
        fields=('url', 'upload_receipt_date', 'uploaded_photo')

class ReservationRoomCharacteristicsSerializer(serializers.ModelSerializer):
    room_type=serializers.SerializerMethodField()
    duration=serializers.SerializerMethodField()
    price_currency=serializers.CharField(source='price_currency.symbol')
    dormitory=ReservationDormitorySerializer()

    def get_room_type(self, obj):
        return str(obj.room_type)

    def get_duration(self, obj):
        return str(obj.duration)

    class Meta:
        model=models.RoomCharacteristics
        fields=('id', 'price', 'price_currency',
                  'room_type', 'duration', 'people_allowed_number',
                  'dormitory')

class ReservationDetailsSerializer(serializers.ModelSerializer):
    reservation_creation_date=serializers.DateField(format = '%Y-%m-%d')
    confirmation_deadline_date=serializers.SerializerMethodField()
    last_update_date=serializers.DateField(format = '%Y-%m-%d')

    user=UserSerializer()
    room_characteristics=ReservationRoomCharacteristicsSerializer()
    receipts=ReceiptSerializer(many = True)

    def get_confirmation_deadline_date(self, obj):
        # we show an extra day for the client

        confirmation_deadline_date = obj.confirmation_deadline_date + datetime.timedelta(days=1)
        return (confirmation_deadline_date).strftime('%Y-%m-%d')

    class Meta:
        model=models.Reservation
        fields=('id',
                  'reservation_creation_date', 'confirmation_deadline_date', 'status',
                  'last_update_date', 'follow_up_message',
                  'user', 'room_characteristics', 'receipts')

class ClientAcceptedReservationSerializer(serializers.Serializer):
    room_id=serializers.IntegerField()

    def create(self, validated_data):
        room_id=validated_data.get('room_id', None)
        user=self.context['request'].user

        room_characteristics=models.RoomCharacteristics.objects.get(pk = room_id)
        instance=models.Reservation.create(user = user, room_characteristics = room_characteristics)
        instance.save()

        return instance

    class Meta:
        fields=('room_id')

class ClientReservationManagementSerializer(serializers.ModelSerializer):
    confirmation_deadline_date=serializers.DateField(format = '%Y-%m-%d', required = False)
    status=serializers.IntegerField(required = False)
    follow_up_message=serializers.CharField(required = False)

    def update(self, instance, validated_data):
        status=validated_data.get('status', None)
        status=str(status)
        if status:
            if status not in models.Reservation.STATUS_CHARS_LIST:
                raise serializers.ValidationError(i18n.t('student.errorMessages.manageReservation.statusDoesntExist'))
            validated_data['status']=status

        instance.last_update_date=datetime.date.today()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

    class Meta:
        model=models.Reservation
        fields=('confirmation_deadline_date', 'status', 'follow_up_message')

class ReservationManagementDetailsSerializer(serializers.ModelSerializer):
    reservation_creation_date=serializers.DateField(format = '%Y-%m-%d')
    confirmation_deadline_date=serializers.DateField(format = '%Y-%m-%d')
    last_update_date=serializers.DateField(format = '%Y-%m-%d')

    student_name=serializers.CharField(source='user.first_name')
    student_email=serializers.CharField(source='user.email')

    room_id = serializers.IntegerField(source='room_characteristics.id')
    room_price=serializers.IntegerField(source='room_characteristics.price')
    room_price_currency=serializers.CharField(source='room_characteristics.price_currency.symbol')
    room_type=serializers.SerializerMethodField()
    room_duration=serializers.SerializerMethodField()
    room_people_allowed_number=serializers.IntegerField(source='room_characteristics.people_allowed_number')

    def get_room_type(self, obj):
        return str(obj.room_characteristics.room_type)

    def get_room_duration(self, obj):
        return str(obj.room_characteristics.duration)

    receipts=ReceiptSerializer(many = True)

    class Meta:
        model=models.Reservation
        fields=('id',
                  'reservation_creation_date', 'confirmation_deadline_date', 'status',
                  'is_reviewed', 'is_reviewable',
                  'last_update_date', 'follow_up_message',
                  'student_name', 'student_email', 
                  'room_id', 'room_price', 'room_price_currency', 
                  'room_type', 'room_duration', 'room_people_allowed_number',
                  'receipts')


class ReservationManagementSerializer(serializers.Serializer):
    pending_reservations = serializers.IntegerField(default=0, read_only=True)
    rejected_reservations = serializers.IntegerField(default=0, read_only=True)
    confirmed_reservations = serializers.IntegerField(default=0, read_only=True)
    waiting_for_manager_action_reservations = serializers.IntegerField(default=0, read_only=True)
    manager_updated_reservations = serializers.IntegerField(default=0, read_only=True)
    expired_reservations = serializers.IntegerField(default=0, read_only=True)

    reservations=ReservationManagementDetailsSerializer(many = True)

    class Meta:
        fields=('pending_reservations', 'rejected_reservations',
                  'confirmed_reservations', 'waiting_for_manager_action_reservations',
                  'manager_updated_reservations', 'expired_reservations',
                  'reservations')


class RegisterSerializer(serializers.Serializer):
    email=serializers.EmailField(required = allauth_settings.EMAIL_REQUIRED)
    name=serializers.CharField(required = True, write_only = True)
    password1=serializers.CharField(required = True, write_only = True)
    password2=serializers.CharField(required = True, write_only = True)

    def validate_email(self, email):
        email=get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(i18n.t('student.errorMessages.auth.emailAlreadyExists'))

        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(i18n.t('student.errorMessages.auth.twoPasswordShouldMatch'))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user


class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if not email_address_exists(email):
            raise serializers.ValidationError(i18n.t('student.errorMessages.auth.noEmailFound'))
        return email

    def save(self, *args, **kwargs):
        request = self.context.get('request')

        current_site = get_current_site(request)
        email = self.validated_data['email']

        user = models.User.objects.get(email__iexact=email)

        token_generator = kwargs.get(
            'token_generator', default_token_generator)
        temp_key = token_generator.make_token(user)

        path = f'/reset-password/{user_pk_to_url_str(user)}/{temp_key}'
        url = settings.BASE_URL + path
        context = {'current_site': current_site,
                   'user': user,
                   'password_reset_url': url,
                   'request': request}

        get_adapter().send_mail(
            'account/email/password_reset_key',
            email,
            context)

        return email

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    key = serializers.CharField()

    def validate_new_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, attrs):
        self.user_token_form = UserTokenForm(
            data={'uidb36': attrs['uid'], 'key': attrs['key']})

        if not self.user_token_form.is_valid():
            raise serializers.ValidationError(i18n.t('student.errorMessages.auth.invalidToken'))

        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError(i18n.t('student.errorMessages.auth.twoPasswordShouldMatch'))

        self.password = attrs['new_password1']

        return attrs

    def save(self):
        user = self.user_token_form.reset_user
        get_adapter().set_password(user, self.password)
        return user



class ResendConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password_reset_form_class = ResetPasswordForm

    def validate(self, attrs):
        self.reset_form = self.password_reset_form_class(
            data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return attrs

    def save(self):
        request = self.context.get('request')
        email = self.reset_form.cleaned_data['email']
        user = models.User.objects.get(email__iexact=email)
        send_email_confirmation(request, user, True)
        return email


class FeatureFilterSerializer(serializers.ModelSerializer):
    # name = I18nField()
    name = serializers.SerializerMethodField()
    icon = serializers.CharField(default='fa-check')

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        model = models.FeatureFilter
        fields = ('id', 'name', 'icon')


class IntegralFilterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_checkbox = serializers.BooleanField(default=False)
    is_integral = serializers.BooleanField(default=True)
    is_optional = serializers.BooleanField()
    value = serializers.SerializerMethodField()
    min_value = serializers.SerializerMethodField()
    max_value = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.name)

    def get_value(self, obj):
        result = obj.integralfilter.integral_choices.aggregate(
            django_models.Max('selected_number'), django_models.Min('selected_number'))

        self.min_value = result['selected_number__min']
        self.max_value = result['selected_number__max']

        return [self.min_value, self.max_value]

    def get_min_value(self, obj):
        return self.min_value

    def get_max_value(self, obj):
        return self.max_value

    class Meta:
        model = models.IntegralFilter
        fields = ('id', 'name', 'is_checkbox', 'is_integral', 'is_optional',
                  'value', 'min_value', 'max_value')


class RadioOptionSerializer(serializers.ModelSerializer):
    # name = I18nField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        model = models.RadioOption
        fields = ('id', 'name')


class RadioFilterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_checkbox = serializers.BooleanField(default=True)
    is_integral = serializers.BooleanField(default=False)
    options = RadioOptionSerializer(many=True)
    is_optional = serializers.BooleanField()

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        model = models.RadioFilter
        fields = ('id', 'name', 'is_checkbox', 'is_integral', 'options', 'is_optional')


class AddtionalFiltersSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        models.IntegralFilter: IntegralFilterSerializer,
        models.RadioFilter: RadioFilterSerializer,
    }


class DormitoryCategorySerializer(serializers.ModelSerializer):
    # name = I18nField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        model = models.DormitoryCategory
        fields = ('id', 'name')

class DormManagementRoomDetailsRadioFilterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    options = RadioOptionSerializer(many=True)
    chosen_option_id = serializers.IntegerField()
    is_optional = serializers.BooleanField()

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        model = models.RadioFilter
        fields = ('id', 'name', 'options', 'chosen_option_id', 'is_optional')

class DormManagementRoomDetailsIntegralFilterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    selected_number = serializers.IntegerField()
    is_optional = serializers.BooleanField()

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        model = models.IntegralFilter
        fields = ('id', 'name', 'selected_number', 'is_optional')

class DormManagementRoomDetailsSerializer(serializers.ModelSerializer):
    price_currency_id = serializers.IntegerField(source='price_currency.id')
    room_type_id = serializers.SerializerMethodField()
    duration_id = serializers.SerializerMethodField()

    photos = PhotoSerializer(many=True)

    room_types = serializers.SerializerMethodField()
    durations = serializers.SerializerMethodField()
    currencies = serializers.SerializerMethodField()

    radio_filters = serializers.SerializerMethodField()
    integral_filters = serializers.SerializerMethodField()
    all_features = serializers.SerializerMethodField()
    chosen_features = serializers.SerializerMethodField()

    def get_room_type_id(self, obj):
        return obj.radio_choices.get(related_filter__name__contains='Room Type').selected_option.id

    def get_duration_id(self, obj):
        return obj.radio_choices.get(related_filter__name__contains='Duration').selected_option.id

    def get_room_types(self, obj):
        duration_filter = models.Filter.objects.filter(name__contains='Room Type').first()
        return RadioOptionSerializer(duration_filter.options, many=True).data

    def get_durations(self, obj):
        duration_filter = models.Filter.objects.filter(name__contains='Duration').first()
        return RadioOptionSerializer(duration_filter.options, many=True).data

    def get_currencies(self, obj):
        currencies = models.Currency.objects.all()
        return CurrencySerializer(currencies, many=True).data

    def get_radio_filters(self, obj):
        return DormManagementRoomDetailsRadioFilterSerializer(obj.radio_filters, many=True).data

    def get_integral_filters(self, obj):
        return DormManagementRoomDetailsIntegralFilterSerializer(obj.integral_filters, many=True).data

    def get_all_features(self, obj):
        return FeatureFilterSerializer(obj.all_features, many=True).data

    def get_chosen_features(self, obj):
        return obj.features.values_list('id', flat=True)
    

    class Meta:
        model = models.RoomCharacteristics
        fields = ('total_quota', 'allowed_quota', 'room_confirmation_days', 'is_ready',
                  'price', 'price_currency_id', 'room_type_id', 'people_allowed_number', 'duration_id',
                  'photos',
                  'room_types', 'durations', 'currencies',
                  'radio_filters', 'integral_filters', 'all_features', 'chosen_features')

class DormManagementRoomStatisticsSerializer(serializers.ModelSerializer):
    room_type = serializers.SerializerMethodField()
    reserved_rooms_number = serializers.IntegerField()

    def get_room_type(self, obj):
        return str(obj.room_type)

    class Meta:
        model = models.RoomCharacteristics
        fields = ('id', 'room_type', 'total_quota', 'allowed_quota', 'is_ready',
                  'reserved_rooms_number')

class DormManagementRoomIntegralChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    selected_number = serializers.IntegerField()

    class Meta:
        fields = ('id', 'selected_number')

class DormManagementEditRoomSerializer(serializers.Serializer):
    total_quota = serializers.IntegerField(required=False)
    allowed_quota = serializers.IntegerField(required=False)
    room_confirmation_days = serializers.IntegerField(required=False)
    is_ready = serializers.BooleanField(required=False)

    room_type_id = serializers.IntegerField(required=False)
    people_allowed_number = serializers.IntegerField(required=False)

    price = serializers.IntegerField(required=False)
    currency_id = serializers.IntegerField(required=False)

    duration_id = serializers.IntegerField(required=False)

    room_features = serializers.ListField(child=serializers.IntegerField(), required=False)
    radio_options = serializers.ListField(child=serializers.IntegerField(), required=False)
    integral_choices = DormManagementRoomIntegralChoiceSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        direct_assignment_attributes = ['total_quota', 'allowed_quota', 
                                        'room_confirmation_days', 'is_ready']
        for attr in direct_assignment_attributes:
            value = validated_data.get(attr, None)
            if value is not None:
                setattr(instance, attr, value)

        price_cuurency_id = validated_data.get('currency_id', None)
        if price_cuurency_id:
            price_currency = models.Currency.objects.get(pk=price_cuurency_id)
            instance.price_currency = price_currency

        room_features = validated_data.get('room_features', None)
        if room_features:
            features_objects = list(models.FeatureFilter.objects.filter(id__in=room_features).all())
            instance.features.set(features_objects)




        radio_options = validated_data.get('radio_options', [])

        room_type_id = validated_data.get('room_type_id', None)
        if room_type_id:
            radio_options.append(room_type_id)

        duration_id = validated_data.get('duration_id', None)
        if duration_id:
            radio_options.append(duration_id)


        if radio_options:
            radio_choices_objects = []

            for radio_option in radio_options:
                radio_option_object = models.RadioOption.objects.get(pk=radio_option)
                radio_choice_object, _ = (
                    models.RadioChoice.objects.get_or_create(selected_option=radio_option_object, 
                                          related_filter=radio_option_object.related_filter))
                radio_choices_objects.append(radio_choice_object)

            for radio_choice_object in radio_choices_objects:
                previous_radio_choice = instance.radio_choices.filter(related_filter_id=radio_choice_object.related_filter.id).first()
                if previous_radio_choice:
                    instance.radio_choices.remove(previous_radio_choice)
                instance.radio_choices.add(radio_choice_object)




        integral_choices = validated_data.get('integral_choices', [])

        people_allowed_number = validated_data.get('people_allowed_number', None)
        if people_allowed_number:
            integral_choices.append({'selected_number': people_allowed_number, 
                                     'id': models.IntegralFilter.objects.get(name__contains='People Allowed Number')})

        price = validated_data.get('price', None)
        if price:
            integral_choices.append({'selected_number': price, 
                                     'id': models.IntegralFilter.objects.get(name__contains='Price')})

        if integral_choices:
            for integral_choice in integral_choices:
                integral_choice_object, _ = (
                    models.IntegralChoice.objects.get_or_create(selected_number=integral_choice['selected_number'], 
                                          related_filter=models.IntegralFilter.objects.get(pk=integral_choice['id']))
                )
                previous_integral_choice = instance.integral_choices.filter(related_filter_id=integral_choice_object.related_filter.id).first()
                if previous_integral_choice:
                    instance.integral_choices.remove(previous_integral_choice)
                instance.integral_choices.add(integral_choice_object)



        instance.save()

        return instance


    class Meta:
        fields = ('total_quota', 'allowed_quota', 'confirmation_days', 'is_ready',
                  'room_type_id', 'people_allowed_number',
                  'price', 'currency_id',
                  'duration_id',
                  'room_features', 'radio_choices', 'integral_choices')

class DormManagementNewRoomSerializer(serializers.Serializer):
    total_quota = serializers.IntegerField()
    allowed_quota = serializers.IntegerField()
    room_confirmation_days = serializers.IntegerField()
    is_ready = serializers.BooleanField()

    room_type_id = serializers.IntegerField()
    people_allowed_number = serializers.IntegerField()

    price = serializers.IntegerField()
    currency_id = serializers.IntegerField()

    duration_id = serializers.IntegerField()

    room_features = serializers.ListField(child=serializers.IntegerField(), required=False)
    radio_options = serializers.ListField(child=serializers.IntegerField(), required=False)
    integral_choices = DormManagementRoomIntegralChoiceSerializer(many=True, required=False)

    def create(self, validated_data):

        dormitory = models.Dormitory.objects.get(pk=self.context.get('dorm_pk'))

        features_objects = []
        radio_choices_objects = []
        integral_choices_objects = []

        price_currency = models.Currency.objects.get(pk=validated_data['currency_id'])
        validated_data.pop('currency_id', None)

        room_features = validated_data.get('room_features', None)
        if room_features:
            features_objects = list(models.FeatureFilter.objects.filter(id__in=room_features).all())
            validated_data.pop('room_features', None)




        radio_options = validated_data.get('radio_options', [])
        if radio_options:
            validated_data.pop('radio_options', None)

        radio_options.append(validated_data['room_type_id'])
        validated_data.pop('room_type_id', None)

        radio_options.append(validated_data['duration_id'])
        validated_data.pop('duration_id', None)

        for radio_option in radio_options:
            radio_option_object = models.RadioOption.objects.get(pk=radio_option)
            radio_choice_object, _ = (
                models.RadioChoice.objects.get_or_create(selected_option=radio_option_object, 
                                      related_filter=radio_option_object.related_filter))
            radio_choices_objects.append(radio_choice_object)
        


        integral_choices = validated_data.get('integral_choices', [])
        if integral_choices:
            validated_data.pop('integral_choices', None)
        
        integral_choices.append({'selected_number': validated_data['people_allowed_number'], 'id': models.IntegralFilter.objects.get(name__contains='People Allowed Number')})
        validated_data.pop('people_allowed_number', None)

        integral_choices.append({'selected_number': validated_data['price'], 'id': models.IntegralFilter.objects.get(name__contains='Price')})
        validated_data.pop('price', None)

        for integral_choice in integral_choices:
            integral_choice_object, _ = (
                models.IntegralChoice.objects.get_or_create(selected_number=integral_choice['selected_number'], 
                                      related_filter=models.IntegralFilter.objects.get(pk=integral_choice['id'])))
            integral_choices_objects.append(integral_choice_object)



        instance = models.RoomCharacteristics(dormitory=dormitory, 
                                              price_currency=price_currency,
                                              **validated_data)

        instance.save()
        instance = models.RoomCharacteristics.objects.get(pk=instance.id)

        instance.features.set(features_objects)
        instance.radio_choices.set(radio_choices_objects)
        instance.integral_choices.set(integral_choices_objects)

        return instance


    class Meta:
        fields = ('total_quota', 'allowed_quota', 'confirmation_days', 'is_ready',
                  'room_type_id', 'people_allowed_number',
                  'price', 'currency_id',
                  'duration_id',
                  'room_features', 'radio_choices', 'integral_choices')

class DormManagementRoomFiltersSerializer(serializers.Serializer):
    room_types = serializers.SerializerMethodField()
    currencies = serializers.SerializerMethodField()
    durations = serializers.SerializerMethodField()
    room_features = serializers.SerializerMethodField()
    additional_filters = serializers.SerializerMethodField()

    def get_room_types(self, obj):
        room_type_filter = models.Filter.objects.filter(name__contains='Room Type').first()
        return RadioOptionSerializer(room_type_filter.options, many=True).data

    def get_currencies(self, obj):
        currencies = models.Currency.objects.all()
        return CurrencySerializer(currencies, many=True).data

    def get_durations(self, obj):
        duration_filter = models.Filter.objects.filter(name__contains='Duration').first()
        return RadioOptionSerializer(duration_filter.options, many=True).data

    def get_room_features(self, obj):
        filters = models.Filter.objects.room_features()
        return FeatureFilterSerializer(filters, many=True).data

    def get_additional_filters(self, obj):
        filters = (
            models.Filter.objects.additional_filters().exclude(
                django_models.Q(name__contains='Duration') | 
                django_models.Q(name__contains='Room Type') |
                django_models.Q(name__contains='Price') | 
                django_models.Q(name__contains='People Allowed Number'))
        )
        return AddtionalFiltersSerializer(filters, many=True).data

class ClientReturnedFiltersSerializer(serializers.Serializer):
    category_options = serializers.SerializerMethodField()
    duration_options = serializers.SerializerMethodField()
    additional_filters = serializers.SerializerMethodField()
    dorm_features = serializers.SerializerMethodField()
    room_features = serializers.SerializerMethodField()

    def get_category_options(self, obj):
        categories = models.DormitoryCategory.objects.all()
        return DormitoryCategorySerializer(categories, many=True).data

    def get_duration_options(self, obj):
        duration_filter = models.Filter.objects.filter(name__contains='Duration').first()
        return RadioOptionSerializer(duration_filter.options, many=True).data

    def get_additional_filters(self, obj):
        filters = models.Filter.objects.additional_filters()
        return AddtionalFiltersSerializer(filters, many=True).data

    def get_dorm_features(self, obj):
        filters = models.Filter.objects.dorm_features()
        return FeatureFilterSerializer(filters, many=True).data

    def get_room_features(self, obj):
        filters = models.Filter.objects.room_features()
        return FeatureFilterSerializer(filters, many=True).data


class ClientAdditionalFiltersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    choosen_options_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    min_value = serializers.IntegerField(required=False)
    max_value = serializers.IntegerField(required=False)

    class Meta:
        model = models.RadioFilter
        fields = ('id', 'choosen_options_ids', 'min_value', 'max_value')


class ClientAcceptedFiltersSerializer(serializers.Serializer):
    category_selected_option_id = serializers.IntegerField(required=False)
    duration_option_id = serializers.IntegerField(required=False)
    additional_filters = ClientAdditionalFiltersSerializer(many=True, required=False)
    dorm_features = serializers.ListField(child=serializers.IntegerField(), required=False)
    room_features = serializers.ListField(child=serializers.IntegerField(), required=False)


class RoomFeaturesSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        fields = ('name')


class RadioChoiceSerializer(serializers.ModelSerializer):
    filter_name = serializers.SerializerMethodField()
    choice = serializers.SerializerMethodField()

    def get_filter_name(self, obj):
        return str(obj.related_filter.name)

    def get_choice(self, obj):
        return str(obj.selected_option.name)

    class Meta:
        model = models.RadioChoice
        fields = ('filter_name', 'choice')


class IntegralChoiceSerializer(serializers.ModelSerializer):
    filter_name = serializers.SerializerMethodField()
    choice = serializers.SerializerMethodField()

    def get_filter_name(self, obj):
        return str(obj.related_filter.name)

    def get_choice(self, obj):
        return obj.selected_number

    class Meta:
        model = models.IntegralChoice
        fields = ('filter_name', 'choice')


class ChoiceSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        models.IntegralChoice: IntegralChoiceSerializer,
        models.RadioChoice: RadioChoiceSerializer,
    }


class ClientPhotoRoomSerializer(serializers.Serializer):
    uploaded_photo = serializers.ImageField(required=False)
    url = serializers.URLField(required=False)
    is_3d = serializers.BooleanField(default=False)

    def create(self, validated_data):
        room_characteristics = models.RoomCharacteristics.objects.get(pk=self.context.get('view').kwargs.get('room_pk'),
                                                      dormitory_id=self.context.get('view').kwargs.get('dorm_pk'))
        uploaded_photo = validated_data.get('uploaded_photo', None)
        
        url = validated_data.get('url', None)
        
        if not url and not uploaded_photo:
            raise serializers.ValidationError(i18n.t('student.errorMessages.manageDorm.pleaseAddEitherURLorPhoto'))

        if url:
            if not validated_data['is_3d']:
                raise serializers.ValidationError(i18n.t('student.errorMessages.manageDorm.urlOnlyWith3D'))
            instance = models.RoomPhoto(photo=url, is_3d=True, room_characteristics=room_characteristics)

        else:
            instance = models.RoomPhoto(photo=uploaded_photo, room_characteristics=room_characteristics)

        instance.save()

        return instance

    class Meta:
        fields = ('uploaded_photo', 'url', 'is_3d')

class ClientPhotoDormSerializer(serializers.Serializer):
    uploaded_photo = serializers.ImageField(required=False)
    url = serializers.URLField(required=False)
    is_3d = serializers.BooleanField(default=False)

    def create(self, validated_data):
        dormitory = models.Dormitory.objects.get(pk=self.context.get('view').kwargs.get('dorm_pk'))
        uploaded_photo = validated_data.get('uploaded_photo', None)
        
        url = validated_data.get('url', None)
        
        if not url and not uploaded_photo:
            raise serializers.ValidationError(i18n.t('student.errorMessages.manageDorm.pleaseAddEitherURLorPhoto'))

        if url:
            if not validated_data['is_3d']:
                raise serializers.ValidationError(i18n.t('student.errorMessages.manageDorm.urlOnlyWith3D'))
            instance = models.DormitoryPhoto(photo=url, is_3d=True, dormitory=dormitory)

        else:
            instance = models.DormitoryPhoto(photo=uploaded_photo, dormitory=dormitory)

        instance.save()

        return instance

    class Meta:
        fields = ('uploaded_photo', 'url', 'is_3d')


class RoomSerializer(serializers.ModelSerializer):
    rooms_left = serializers.IntegerField(source='allowed_quota')

    photos = PhotoSerializer(many=True)

    room_type = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    choices = serializers.SerializerMethodField()
    features = RoomFeaturesSerializer(many=True)

    def get_room_type(self, obj):
        return str(obj.room_type)

    def get_duration(self, obj):
        return str(obj.duration)

    def get_choices(self, obj):
        radio_choices = (
            django_models.Q(id__in=obj.radio_choices.all().exclude(
                django_models.Q(related_filter__name__contains='Duration') | 
                django_models.Q(related_filter__name__contains='Room Type')))
                )

        integral_choices = (
            django_models.Q(id__in=obj.integral_choices.all().exclude(
                django_models.Q(related_filter__name__contains='Price') | 
                django_models.Q(related_filter__name__contains='People Allowed Number')))
                )
        choices = models.Choice.objects.filter(radio_choices | integral_choices)
        return ChoiceSerializer(choices, many=True).data

    class Meta:
        model = models.RoomCharacteristics
        fields = ('id', 'rooms_left',
                  'photos',
                  'price', 'duration', 'room_type', 'people_allowed_number',
                  'choices', 'features')


class ClientBankAccountSerializer(serializers.Serializer):
    bank_name = serializers.CharField(required=False)
    account_name = serializers.CharField(required=False)
    account_number = serializers.CharField(required=False)
    swift = serializers.CharField(required=False)
    iban = serializers.CharField(required=False)
    currency_code = serializers.CharField(required=False)

    def create(self, validated_data):
        dormitory = models.Dormitory.objects.get(pk=self.context.get('view').kwargs.get('dorm_pk'))
        currency = models.Currency.objects.get(code=validated_data['currency_code'])

        validated_data.pop('currency_code', None)
        validated_data['dormitory'] = dormitory
        validated_data['currency'] = currency

        instance = models.BankAccount(**validated_data)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    class Meta:
        fields = ('bank_name', 'account_name',
                  'account_number', 'swift', 'iban', 'currency_code')


class ClientDormManagementSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    abouts = serializers.ListField(child=I18nField(), required=False)
    features = serializers.ListField(child=serializers.IntegerField(), required=False)
    cover = serializers.ImageField(required=False)
    geo_longitude = serializers.CharField(required=False)
    geo_latitude = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    contact_name = serializers.CharField(required=False)
    contact_email = serializers.CharField(required=False)
    contact_number = serializers.CharField(required=False)
    contact_fax = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        
        abouts = validated_data.get('abouts', None)
        if abouts:
            for about in abouts:
                about_data = about.data.items()
                for language_code, text in about_data:
                    #print(language_code, 'zzz', text)
                    instance.about.data[language_code] = text
            validated_data.pop('abouts', None)

        cover = validated_data.get('cover', None)
        if cover:
            instance.cover = cover
            validated_data.pop('cover', None)

        features = validated_data.get('features', None)
        if features:
            instance.features.clear()
            for feature_id in features:
                feature = models.FeatureFilter.objects.get(pk=feature_id)
                instance.features.add(feature)
        validated_data.pop('features', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

    class Meta:
        model = models.Dormitory
        fields = ('name', 'abouts', 'features',
                  'cover', 'photos',
                  'geo_longitude', 'geo_latitude', 'address',
                  'contact_name', 'contact_email', 'contact_number', 'contact_fax')


class DormManagementSerializer(serializers.ModelSerializer):
    cover = LocalRemoteURLField(source='cover.path')

    class Meta:
        model = models.Dormitory
        fields = ('id', 'name', 'cover')


class DormManagementDetailsSerializer(serializers.ModelSerializer):
    cover = LocalRemoteURLField(source='cover.path')

    bank_accounts = BankAccountSerializer(many=True)
    features = FeatureFilterSerializer(many=True)
    photos = PhotoSerializer(many=True)
    abouts = serializers.SerializerMethodField()
    all_features = serializers.SerializerMethodField()

    def get_abouts(self, obj):
        return obj.about.data

    def get_all_features(self, obj):
        all_dorm_features = models.Filter.objects.dorm_features()
        return FeatureFilterSerializer(all_dorm_features, many=True).data

    class Meta:
        model = models.Dormitory
        fields = ('name', 'abouts', 'bank_accounts', 'all_features', 'features',
                  'cover', 'photos',
                  'geo_longitude', 'geo_latitude', 'address',
                  'contact_name', 'contact_email', 'contact_number', 'contact_fax')


class DormSerializer(serializers.ModelSerializer):
    cover = LocalRemoteURLField(source='cover.path')

    rooms_left_in_dorm = serializers.IntegerField()

    number_of_reviews = serializers.IntegerField()
    stars_average = serializers.DecimalField(decimal_places=1, max_digits=2)

    features = FeatureFilterSerializer(many=True)
    room_characteristics = RoomSerializer(many=True)

    class Meta:
        model = models.Dormitory
        fields = ('id', 'name', 'cover',
                  'number_of_reviews', 'stars_average',
                  'geo_longitude', 'geo_latitude', 'address',
                  'rooms_left_in_dorm',
                  'features', 'room_characteristics')


class DormDetailsSerializer(serializers.ModelSerializer):
    main_info = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True)
    about = serializers.SerializerMethodField()
    room_characteristics = RoomSerializer(many=True)
    number_of_reviews = serializers.IntegerField()
    stars_average = serializers.DecimalField(decimal_places=1, max_digits=2)
    reviews = ReviewSerializer(many=True)

    def get_main_info(self, obj):
        return DormSerializer(obj).data

    def get_about(self, obj):
        return str(obj.about)

    def get_features(self, obj):
        filters = models.Filter.objects.dorm_features()
        return FeatureFilterSerializer(filters, many=True).data

    class Meta:
        model = models.Dormitory
        fields = ('main_info',
                  'photos',
                  'about', 'contact_name', 'contact_email', 'contact_number', 'contact_fax',
                  'features',
                  'number_of_reviews', 'stars_average', 'reviews',
                  'room_characteristics')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = ('id', 'symbol', 'code',)


class LanguageSerailizer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()


class LocaleSerailizer(serializers.Serializer):
    currencies = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()

    def get_currencies(self, obj):
        currencies = models.Currency.objects.all()
        return CurrencySerializer(currencies, many=True).data

    def get_languages(self, obj):
        languages = [{'code': code, 'name': name} for code, name in settings.LANGUAGES]

        return LanguageSerailizer(languages, many=True).data
