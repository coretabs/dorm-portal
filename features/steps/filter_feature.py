from django.test import TestCase
from behave import given, when, then

from api.engine.models import Dormitory, RoomCharacteristics, RadioFilter, Option, FeatureChoice

def create_dorm_features(self):
    self.swimming_pool = FeatureChoice(name='Swimming pool', is_dorm_feature=True)
    self.free_wifi = FeatureChoice(name='Free WiFi', is_dorm_feature=True)

    self.swimming_pool.save()
    self.free_wifi.save()

    self.swimming_pool = FeatureChoice.objects.filter(name='Swimming pool').first()
    self.free_wifi = FeatureChoice.objects.filter(name='Free WiFi').first()


@given('we have 2 dormitory with different features')
def prepare_dormitory(self):

    create_dorm_features(self)

    self.alfam = Dormitory(name='Alfam')
    self.alfam.save()

    self.alfam.features.add(self.swimming_pool)
    self.alfam.save()

    self.dovec = Dormitory(name='Dovec')
    self.dovec.save()

    self.dovec.features.add(self.free_wifi)
    self.dovec.save()


@when('filtering dorms by swimming pool')
def filtering(self):
    filters = [self.swimming_pool.get_query(), ]
    self.filtered_dorm_alfam = Dormitory.objects.apply_dorm_filters(filters)


@then('get only the dorm which has swimming pool')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().name == 'Alfam'
    assert self.filtered_dorm_alfam.all().count() == 1


def create_room_features(self):
    self.luxury_shower = FeatureChoice(name='Luxury shower')
    self.luxury_shower.save()
    self.luxury_shower = FeatureChoice.objects.filter(name='Luxury shower').first()

    self.air_conditioner = FeatureChoice(name='Air Conditioner')
    self.air_conditioner.save()
    self.air_conditioner = FeatureChoice.objects.filter(name='Air Conditioner').first()


@given('we have 2 dormitoroes with room-specific features')
def prepare_dormitory(self):

    create_room_features(self)

    self.alfam = Dormitory(name='Alfam')
    self.alfam.save()

    self.room1 = RoomCharacteristics(dormitory=self.alfam)
    self.room1.save()
    self.room1.features.add(self.luxury_shower, self.air_conditioner)
    self.room1.save()

    self.room2 = RoomCharacteristics(dormitory=self.alfam)
    self.room2.save()
    self.room2.features.add(self.air_conditioner)
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
    assert self.filtered_dorms.first().room_characteristics.first().features.first().name == 'Luxury shower'


@when('filtering dorms by luxury shower & air conditioner')
def filtering(self):
    filters = [self.luxury_shower.get_query(), self.air_conditioner.get_query(), ]
    self.filtered_dorms = Dormitory.objects.apply_room_filters(filters)


@then('get only alfam with just one rooms having luxury shower & air conditioner')
def test_model_can_create_a_message(self):
    assert self.filtered_dorms.first().name == 'Alfam'
    assert self.filtered_dorms.count() == 1

    assert self.filtered_dorms.first().room_characteristics.all().count() == 1
    assert self.filtered_dorms.first().room_characteristics.first().features.all()[0].name == 'Luxury shower'
    assert self.filtered_dorms.first().room_characteristics.first().features.all()[1].name == 'Air Conditioner'


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
    assert self.filtered_dorms.first().room_characteristics.all()[0].features.filter(name='Air Conditioner').count() == 1
    assert self.filtered_dorms.first().room_characteristics.all()[1].features.filter(name='Air Conditioner').count() == 1
