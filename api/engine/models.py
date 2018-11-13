from functools import reduce

from django.db import models

from polymorphic.models import PolymorphicModel

from django.db import models as django_models


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
        combined_filters = reduce(lambda filter1, filter2: filter1 & filter2, filters)
        dorms = self.filter(combined_filters)

        return dorms

    def available(self):
        return self.filter(room_characteristics__allowed_quota__gte = 1)


class Choice(PolymorphicModel):
    name = models.CharField(max_length=60)


class RadioChoice(Choice):
    is_optional = models.BooleanField(default=True)

    def get_query(self, selected_options):
        return (models.Q(filters__radiofilter__radio_choice__id = self.id) &
                models.Q(filters__radiofilter__selected_option__id__in = selected_options))

    def __str__(self):
        return f'{self.name} radio choice'


class IntegralChoice(Choice):
    is_optional = models.BooleanField(default=True)

    def get_query(self, min, max):
        return (models.Q(filters__integralfilter__integral_choice__id = self.id) & 
                models.Q(filters__integralfilter__selected_number__gte = min) & 
                models.Q(filters__integralfilter__selected_number__lte = max))

    def __str__(self):
        return f'{self.name} intgeral choice'


class Option(models.Model):
    name = models.CharField(max_length=60)

    radio_choice = models.ForeignKey(
        RadioChoice, related_name='options', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} option for the filter {self.radio_choice.name}'


class Filter(PolymorphicModel):
    pass

class IntegralFilter(Filter):
    selected_number = models.IntegerField(default=0)

    integral_choice = models.ForeignKey(
        IntegralChoice, related_name='integral_filters', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.integral_choice.name} filter with number {self.number}'


class RadioFilter(Filter):
    selected_option = models.ForeignKey(
                        Option, related_name='radio_filters', on_delete=models.CASCADE)
    radio_choice = models.ForeignKey(
                        RadioChoice, related_name='radio_filters', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.radio_choice.name} filter with options {self.options}'


class FeatureChoice(Choice):

    is_dorm_feature = models.BooleanField(default=False)

    def get_query(self):
        return models.Q(features__id=self.id)

    def __str__(self):
        return f'{self.name} filter'


class Dormitory(models.Model):
    PUBLIC = '0'
    PRIVATE = '1'
    CATEGORIES = (
        (PUBLIC, 'public'),
        (PRIVATE, 'private'),
    )

    name = models.CharField(max_length=60)
    about = models.CharField(max_length=1000)

    geo_longitude = models.CharField(max_length=20)
    geo_latitude = models.CharField(max_length=20)
    address = models.CharField(max_length=150)

    category = models.CharField(
        max_length=2, choices=CATEGORIES, default=PUBLIC)

    features = models.ManyToManyField(
        FeatureChoice, related_name='dormitories')

    objects = DormitoryQuerySet.as_manager()

    def __str__(self):
        return f'{self.name}'


class RoomCharacteristics(models.Model):
    total_quota = models.IntegerField(default=0)
    allowed_quota = models.IntegerField(default=0)

    filters = models.ManyToManyField(
        Filter, related_name='filters')

    features = models.ManyToManyField(
        FeatureChoice, related_name='room_characteristics')

    dormitory = models.ForeignKey(
        Dormitory, related_name='room_characteristics', on_delete=models.CASCADE)