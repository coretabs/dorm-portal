from functools import reduce

from django.db import models

from polymorphic.models import PolymorphicModel

from django.db import models as django_models


class DormitoryQuerySet(django_models.QuerySet):
    def apply_filters(self, filters):

        combined_filters = reduce(lambda filter1, filter2: filter1 & filter2, filters)

        filtered_rooms = RoomCharacteristics.objects.filter(combined_filters)

        room_characteristics = django_models.Prefetch(
            'room_characteristics', queryset=filtered_rooms)

        dorms = self.filter(room_characteristics__in=filtered_rooms).prefetch_related(room_characteristics)
        
        return dorms

    def available(self):
        return self.filter(room_characteristics__allowed_quota__gte = 1)


class Dormitory(models.Model):
    PUBLIC = '0'
    PRIVATE = '1'
    CATEGORIES = (
        (PUBLIC, 'public'),
        (PRIVATE, 'private'),
    )

    name = models.CharField(max_length=60)
    history = models.CharField(max_length=1000)

    geo_longitude = models.CharField(max_length=20)
    geo_latitude = models.CharField(max_length=20)
    address = models.CharField(max_length=150)

    category = models.CharField(
        max_length=2, choices=CATEGORIES, default=PUBLIC)

    objects = DormitoryQuerySet.as_manager()

    def __str__(self):
        return f'{self.name}'


class Filter(PolymorphicModel):
    name = models.CharField(max_length=60)


class IntegralFilter(Filter):
    number = models.IntegerField(default=0)

    def get_query(self, min, max):
        return (models.Q(filters__integralfilter__number__gte = min) & 
                models.Q(filters__integralfilter__number__lte = max))

    def __str__(self):
        return f'{self.name} filter with number {self.number}'


class RadioFilter(Filter):

    def get_query(self, selected_options):
        return models.Q(filters__radiofilter__options__name__in = selected_options)

    def __str__(self):
        return f'{self.name} filter with options {self.options}'


class Option(models.Model):
    name = models.CharField(max_length=60)

    radio_filter = models.ForeignKey(
        RadioFilter, related_name='options', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} option for the filter {self.radio_filter.name}'


class RoomCharacteristics(models.Model):
    total_quota = models.IntegerField(default=0)
    allowed_quota = models.IntegerField(default=0)

    filters = models.ManyToManyField(
        Filter, related_name='filters')

    dormitory = models.ForeignKey(
        Dormitory, related_name='room_characteristics', on_delete=models.CASCADE)