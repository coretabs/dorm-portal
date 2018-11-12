from django.test import TestCase
from behave import given, when, then

from api.engine.models import Dormitory, RoomCharacteristics, IntegralFilter, IntegralChoice

def create_price(integral_choice, price):
    result = IntegralFilter(selected_number=price)
    result.integral_choice = integral_choice
    result.save()

    result = IntegralFilter.objects.filter(selected_number=price).first()

    return result

def create_room(dorm, price):
    result = RoomCharacteristics(dormitory=dorm)
    result.save()
    result.filters.add(price)
    result.save()

    return result

@given('we have 4 rooms different prices (alfam: 3 rooms, dovec: 1 room)')
def prepare_dormitory(self):
    self.alfam = Dormitory(name='Alfam')
    self.alfam.save()

    self.integral_choice = IntegralChoice(name='price')
    self.integral_choice.save()

    self.price_alfam1 = create_price(self.integral_choice, 1000)
    self.price_alfam2 = create_price(self.integral_choice, 1200)
    self.price_alfam3 = create_price(self.integral_choice, 1700)

    self.room1 = create_room(self.alfam, self.price_alfam1)
    self.room2 = create_room(self.alfam, self.price_alfam2)
    self.room3 = create_room(self.alfam, self.price_alfam3)

    self.dovec = Dormitory(name='Dovec')
    self.dovec.save()

    self.price_dovec1 = create_price(self.integral_choice, 2000)
    
    self.room4 = create_room(self.dovec, self.price_dovec1)


@when('filtering alfam prices between 500, 1500')
def filtering(self):
    filters = [self.integral_choice.get_query(500, 1500), ]
    self.filtered_dorm_alfam = Dormitory.objects.filter(name='Alfam').apply_room_filters(filters)


@then('get alfam dormitory with just 2 rooms')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().name == 'Alfam'
    assert self.filtered_dorm_alfam.first().room_characteristics.count() == 2


@when('filtering dovec with wrong price range')
def filtering(self):
    filters = [self.integral_choice.get_query(500, 1500), ]
    self.filtered_dorm_dovec = Dormitory.objects.filter(name='Dovec').apply_room_filters(filters)


@then('not getting any dorm in dovec for wrong price')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_dovec.count() == 0