from django.test import TestCase
from behave import given, when, then

from api.engine.models import Dormitory, RoomCharacteristics, IntegralFilter

def create_price(price):
    result = IntegralFilter(name='price', number=price)
    result.save()
    result = IntegralFilter.objects.filter(number=price).first()

    return result

@given('we have 2 dormitories')
def prepare_dormitory(self):
    self.alfam = Dormitory(name='Alfam')
    self.alfam.save()

    self.price_alfam1 = create_price(1000)
    self.price_alfam2 = create_price(1200)

    self.room1 = RoomCharacteristics(dormitory=self.alfam)
    self.room1.save()
    self.room1.filters.add(self.price_alfam1, self.price_alfam2)
    self.room1.save()

    self.dovec = Dormitory(name='Dovec')
    self.dovec.save()

    self.price_dovec1 = create_price(2000)
    
    self.room2 = RoomCharacteristics(dormitory=self.dovec)
    self.room2.save()
    self.room2.filters.add(self.price_dovec1)
    self.room2.save()


@when('filtering alfam right price')
def filtering(self):
    filters = [self.price_alfam1.get_query(500, 1500), self.price_alfam2.get_query(500, 1500), ]
    self.filtered_dorm_alfam = Dormitory.objects.filter(name='Alfam').apply_filters(filters)

@then('get alfam dormitory')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().name == 'Alfam'

@when('filtering dovec wrong price')
def filtering(self):
    filters = [self.price_dovec1.get_query(500, 1500), ]
    self.filtered_dorm_dovec = Dormitory.objects.filter(name='Dovec').apply_filters(filters)

@then('not getting any dorm')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_dovec.count() == 0