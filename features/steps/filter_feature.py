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


@given('we have 2 dormitory with different facilities')
def prepare_dormitory(self):

    create_dorm_activities_facilities(self)

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


def create_room_activities_facilities(self):
    self.luxury_shower = ActivityFacilityFilter(name='Luxury shower')
    self.luxury_shower.save()
    self.luxury_shower = ActivityFacilityFilter.objects.filter(name='Luxury shower').first()

    self.air_conditioner = ActivityFacilityFilter(name='Air Conditioner')
    self.air_conditioner.save()
    self.air_conditioner = ActivityFacilityFilter.objects.filter(name='Air Conditioner').first()


@given('we have 2 dormitoroes with room-specific facilities')
def prepare_dormitory(self):

    create_room_activities_facilities(self)

    self.alfam = Dormitory(name='Alfam')
    self.alfam.save()

    self.room1 = RoomCharacteristics(dormitory=self.alfam)
    self.room1.save()
    self.room1.filters.add(self.luxury_shower, self.air_conditioner)
    self.room1.save()

    self.room2 = RoomCharacteristics(dormitory=self.alfam)
    self.room2.save()
    self.room2.filters.add(self.air_conditioner)
    self.room2.save()

    self.dovec = Dormitory(name='Dovec')
    self.dovec.save()

    self.room3 = RoomCharacteristics(dormitory=self.dovec)
    self.room3.save()


@when('filtering dorms by having one room with luxury shower')
def filtering(self):
    filters = [self.luxury_shower.get_query(), ]
    self.filtered_dorms = Dormitory.objects.apply_room_filters(filters)


@then('get only alfam with just one room which has luxury shower')
def test_model_can_create_a_message(self):
    assert self.filtered_dorms.first().name == 'Alfam'
    assert self.filtered_dorms.count() == 1

    assert self.filtered_dorms.first().room_characteristics.count() == 1
    assert self.filtered_dorms.first().room_characteristics.first().filters.first().name == 'Luxury shower'


@when('filtering dorms by luxury shower & air conditioner')
def filtering(self):
    filters = [self.luxury_shower.get_query(), self.air_conditioner.get_query(), ]
    #breakpoint()
    self.filtered_dorms = Dormitory.objects.apply_room_filters(filters)


@then('get only alfam with just one rooms having luxury shower & air conditioner')
def test_model_can_create_a_message(self):
    assert self.filtered_dorms.first().name == 'Alfam'
    assert self.filtered_dorms.count() == 1

    assert self.filtered_dorms.first().room_characteristics.all().count() == 1
    assert self.filtered_dorms.first().room_characteristics.first().filters.all()[0].name == 'Luxury shower'
    assert self.filtered_dorms.first().room_characteristics.first().filters.all()[1].name == 'Air Conditioner'


@when('filtering dorms by air conditioner')
def filtering(self):
    filters = [self.air_conditioner.get_query(), ]
    self.filtered_dorms = Dormitory.objects.apply_room_filters(filters)


@then('get only alfam with two rooms having air conditioner')
def test_model_can_create_a_message(self):
    assert self.filtered_dorms.first().name == 'Alfam'
    assert self.filtered_dorms.count() == 1

    assert self.filtered_dorms.first().room_characteristics.all().count() == 2
    # use exists
    assert self.filtered_dorms.first().room_characteristics.all()[0].filters.filter(name='Air Conditioner').count() == 1
    assert self.filtered_dorms.first().room_characteristics.all()[1].filters.filter(name='Air Conditioner').count() == 1
