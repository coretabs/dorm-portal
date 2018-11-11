from functools import reduce

from django.db import models

from polymorphic.models import PolymorphicModel

from django.db import models as django_models


class DormitoryQuerySet(django_models.QuerySet):
    def apply_filters(self, filters):
        combined_filters = reduce(lambda filter1, filter2: filter1 & filter2, filters)
        result = self.filter(combined_filters)
        
        return result

class DormitoryManager(django_models.Manager):
    def get_queryset(self):
        return DormitoryQuerySet(self.model, using=self._db)

    def apply_filters(self, filters):
        return self.get_queryset().apply_filters(filters)

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

    objects = DormitoryManager()

    def __str__(self):
        return f'{self.name}'


class Filter(PolymorphicModel):
    name = models.CharField(max_length=60)


class IntegralFilter(Filter):
    number = models.IntegerField(default=0)

    def get_query(self, min, max):
        return (models.Q(room_characteristics__filters__integralfilter__number__gte = min) & 
                models.Q(room_characteristics__filters__integralfilter__number__lte = max))

    def __str__(self):
        return f'{self.name} filter with number {self.number}'


class RoomCharacteristics(models.Model):
    total_quota = models.IntegerField(default=0)
    filters = models.ManyToManyField(
        Filter, related_name='filters')

    dormitory = models.ForeignKey(
        Dormitory, related_name='room_characteristics', on_delete=models.CASCADE)