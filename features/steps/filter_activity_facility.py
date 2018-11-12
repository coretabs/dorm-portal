from django.test import TestCase
from behave import given, when, then

from api.engine.models import Dormitory, RoomCharacteristics, RadioFilter, Option, ActivityFacilityFilter

def create_dorm_activities_facilities(self):
    self.swimming_pool = ActivityFacilityFilter(name='Swimming pool', is_dorm_activity_facility=True)
    self.free_wifi = ActivityFacilityFilter(name='Free WiFi', is_dorm_activity_facility=True)

    self.swimming_pool.save()
    self.free_wifi.save()

    self.swimming_pool = ActivityFacilityFilter.objects.filter(name='Swimming pool').first()
    self.free_wifi = ActivityFacilityFilter.objects.filter(name='Free WiFi').first()

def create_room_activities_facilities(self):
    pass


@given('we have 2 dormitory with different facilities')
def prepare_dormitory(self):

    create_dorm_activities_facilities(self)
    create_room_activities_facilities(self)

    self.alfam = Dormitory(name='Alfam')
    self.alfam.save()

    self.alfam.activities_facilities.add(self.swimming_pool)
    self.alfam.save()

    self.dovec = Dormitory(name='Dovec')
    self.dovec.save()

    self.dovec.activities_facilities.add(self.free_wifi)
    self.dovec.save()


@when('filtering dorms by swimming pool')
def filtering(self):
    filters = [self.swimming_pool.get_query(), ]
    self.filtered_dorm_alfam = Dormitory.objects.apply_dorm_filters(filters)


@then('get only the dorm which has swimming pool')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().name == 'Alfam'
    assert self.filtered_dorm_alfam.all().count() == 1