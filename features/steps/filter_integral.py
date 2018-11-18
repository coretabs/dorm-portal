from behave import given, when, then

from api.engine.models import *

from features.steps.factory import *


@given('we have 4 rooms different prices (alfam: 3 rooms, dovec: 1 room)')
def prepare_dormitory(self):
    category_public = create_category('public')
    self.alfam = create_dorm('Alfam', category_public)

    self.price_filter = IntegralFilter(name='Price')
    self.price_filter.save()

    self.price_alfam1 = create_integral_choice(self.price_filter, 1000)
    self.price_alfam2 = create_integral_choice(self.price_filter, 1200)
    self.price_alfam3 = create_integral_choice(self.price_filter, 1700)

    self.room1 = create_room_with_integral_choices(self.alfam, [self.price_alfam1, ])
    self.room2 = create_room_with_integral_choices(self.alfam, [self.price_alfam2, ])
    self.room3 = create_room_with_integral_choices(self.alfam, [self.price_alfam3, ])

    self.dovec = create_dorm('Dovec', category_public)

    self.price_dovec1 = create_integral_choice(self.price_filter, 2000)
    self.room4 = create_room_with_integral_choices(self.dovec, [self.price_dovec1, ])


@when('filtering alfam prices between 500, 1500')
def filtering(self):
    filters = [self.price_filter.get_query(500, 1500), ]
    self.filtered_dorm_alfam = Dormitory.objects.filter(
        name='Alfam').apply_room_filters(filters)


@then('get alfam dormitory with just 2 rooms')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().name == 'Alfam'
    assert self.filtered_dorm_alfam.first().room_characteristics.count() == 2


@when('filtering dovec with wrong price range')
def filtering(self):
    filters = [self.price_filter.get_query(500, 1500), ]
    self.filtered_dorm_dovec = Dormitory.objects.filter(
        name='Dovec').apply_room_filters(filters)


@then('not getting any dorm in dovec for wrong price')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_dovec.count() == 0
