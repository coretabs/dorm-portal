from functools import reduce

from django.db import models as django_models

from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet


class DormitoryQuerySet(django_models.QuerySet):
    def apply_room_filters(self, filters):

        filtered_rooms = RoomCharacteristics.objects.filter(filters[0])
        for current_filter in filters:
            filtered_rooms = filtered_rooms.filter(current_filter)

        room_characteristics = django_models.Prefetch(
            'room_characteristics', queryset=filtered_rooms)

        dorms = self.filter(room_characteristics__in=filtered_rooms)\
                    .prefetch_related(room_characteristics).distinct()

        return dorms

    def apply_dorm_filters(self, filters):
        combined_filters = reduce(
            lambda filter1, filter2: filter1 & filter2, filters)
        dorms = self.filter(combined_filters)

        return dorms

    def available(self):
        return self.filter(room_characteristics__allowed_quota__gte=1)


class FilterQuerySet(PolymorphicQuerySet):

    def main_filters(self):
        return self.filter(django_models.Q(name='category') | django_models.Q(name='academic year'))

    def radio_filters(self):

        result = self.instance_of(RadioFilter).exclude(django_models.Q(name='category') | django_models.Q(name='academic year'))\
            # .annotate(is_checkbox=django_models.Value(True, output_field=django_models.BooleanField()))\
        # .annotate(is_integral=django_models.Value(False, output_field=django_models.BooleanField()))\
        # .prefetch_related('options')

        return result

    def integral_filters(self):

        result = self.instance_of(IntegralFilter)
        # .annotate(min_value=django_models.Min('integralfilter__integral_choices__selected_number'))\
        # .annotate(max_value=django_models.Max('integralfilter__integral_choices__selected_number'))
        # .annotate(is_checkbox=django_models.Value(False, output_field=django_models.BooleanField()))\
        # .annotate(is_integral=django_models.Value(True, output_field=django_models.BooleanField()))\

        return result

    def additional_filters(self):
        return (self.radio_filters() | self.integral_filters()).distinct()

    def dorm_features(self):
        return self.instance_of(FeatureFilter).filter(featurefilter__is_dorm_feature=True)

    def room_features(self):
        return self.instance_of(FeatureFilter).filter(featurefilter__is_dorm_feature=False)


class Filter(PolymorphicModel):
    name = django_models.CharField(max_length=60)

    objects = PolymorphicManager.from_queryset(FilterQuerySet)()

    def __str__(self):
        return f'{self.name} filter'


class RadioFilter(Filter):
    is_optional = django_models.BooleanField(default=True)

    def get_query(self, selected_options):
        return (django_models.Q(radio_choices__radio_filter__id=self.id) &
                django_models.Q(radio_choices__selected_option__id__in=selected_options))

    def __str__(self):
        return f'{self.name} radio filter'


class IntegralFilter(Filter):
    is_optional = django_models.BooleanField(default=True)

    def get_query(self, min, max):
        return (django_models.Q(integral_choices__integral_filter__id=self.id) &
                django_models.Q(integral_choices__selected_number__gte=min) &
                django_models.Q(integral_choices__selected_number__lte=max))

    def __str__(self):
        return f'{self.name} intgeral filter'


class FeatureFilter(Filter):

    is_dorm_feature = django_models.BooleanField(default=False)

    def get_query(self):
        return django_models.Q(features__id=self.id)

    def __str__(self):
        return f'{self.name} filter'


class Option(django_models.Model):
    name = django_models.CharField(max_length=60)

    radio_filter = django_models.ForeignKey(
        RadioFilter, related_name='options', on_delete=django_models.CASCADE)

    def __str__(self):
        return f'{self.name} option for the filter {self.radio_filter.name}'


class Choice(PolymorphicModel):
    pass


class IntegralChoice(Choice):
    selected_number = django_models.IntegerField(default=0)

    integral_filter = django_models.ForeignKey(
        IntegralFilter, related_name='integral_choices', on_delete=django_models.CASCADE)

    def __str__(self):
        return f'{self.integral_filter.name} choice with number {self.selected_number}'


class RadioChoice(Choice):
    selected_option = django_models.ForeignKey(
        Option, related_name='radio_choices', on_delete=django_models.CASCADE)
    radio_filter = django_models.ForeignKey(
        RadioFilter, related_name='radio_choices', on_delete=django_models.CASCADE)

    def __str__(self):
        return f'{self.radio_filter.name} filter with options {self.options}'


class Dormitory(django_models.Model):
    PUBLIC = '0'
    PRIVATE = '1'
    CATEGORIES = (
        (PUBLIC, 'public'),
        (PRIVATE, 'private'),
    )

    name = django_models.CharField(max_length=60)
    about = django_models.CharField(max_length=1000)

    geo_longitude = django_models.CharField(max_length=20)
    geo_latitude = django_models.CharField(max_length=20)
    address = django_models.CharField(max_length=150)

    category = django_models.CharField(
        max_length=2, choices=CATEGORIES, default=PUBLIC)

    features = django_models.ManyToManyField(
        FeatureFilter, related_name='dormitories')

    objects = DormitoryQuerySet.as_manager()

    def __str__(self):
        return f'{self.name}'


class RoomCharacteristics(django_models.Model):
    total_quota = django_models.IntegerField(default=0)
    allowed_quota = django_models.IntegerField(default=0)

    radio_choices = django_models.ManyToManyField(
        RadioChoice, related_name='radio_choices')

    integral_choices = django_models.ManyToManyField(
        IntegralChoice, related_name='integral_choices')

    features = django_models.ManyToManyField(
        FeatureFilter, related_name='room_characteristics')

    dormitory = django_models.ForeignKey(
        Dormitory, related_name='room_characteristics', on_delete=django_models.CASCADE)
