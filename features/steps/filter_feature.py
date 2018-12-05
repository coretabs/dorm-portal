from behave import given, when, then

from api.engine.models import *

from features.steps.factory import *


@given('we have 2 dormitory with different features')
def prepare_dormitory(self):

    self.swimming_pool = create_dorm_feature('Swimming pool')
    self.free_wifi = create_dorm_feature('Free WiFi')

    category_public = create_category('public')
    self.alfam = create_dorm('Alfam', category_public)

    self.alfam.features.add(self.swimming_pool)
    self.alfam.save()

    self.dovec = create_dorm('Dovec', category_public)

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


@given('we have 2 dormitoroes with room-specific features')
def prepare_dormitory(self):

    self.luxury_shower = create_room_feature('Luxury shower')
    self.air_conditioner = create_room_feature('Air Conditioner')

    self.room1 = create_room_with_features(self.alfam, [self.luxury_shower, self.air_conditioner])
    self.room2 = create_room_with_features(self.alfam, [self.air_conditioner, ])

    self.room3 = create_room(self.dovec)


@when('filtering dorms by having one room with luxury shower')
def filtering(self):
    filters = [self.luxury_shower.get_query(), ]
    self.filtered_dorms = Dormitory.objects.apply_room_filters(filters)


@then('get only alfam with just one room which has luxury shower')
def test_model_can_create_a_message(self):
    assert self.filtered_dorms.first().name == 'Alfam'
    assert self.filtered_dorms.count() == 1

    assert self.filtered_dorms.first().room_characteristics.count() == 1
    assert self.filtered_dorms.first().room_characteristics.first(
    ).features.first().name == 'Luxury shower'


@when('filtering dorms by luxury shower & air conditioner')
def filtering(self):
    filters = [self.luxury_shower.get_query(
    ), self.air_conditioner.get_query(), ]
    self.filtered_dorms = Dormitory.objects.apply_room_filters(filters)


@then('get only alfam with just one rooms having luxury shower & air conditioner')
def test_model_can_create_a_message(self):
    assert self.filtered_dorms.first().name == 'Alfam'
    assert self.filtered_dorms.count() == 1

    assert self.filtered_dorms.first().room_characteristics.all().count() == 1
    assert self.filtered_dorms.first().room_characteristics.first().features.all()[
        0].name == 'Luxury shower'
    assert self.filtered_dorms.first().room_characteristics.first().features.all()[
        1].name == 'Air Conditioner'


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
    assert self.filtered_dorms.first().room_characteristics.all(
    )[0].features.filter(name='Air Conditioner').count() == 1
    assert self.filtered_dorms.first().room_characteristics.all(
    )[1].features.filter(name='Air Conditioner').count() == 1
