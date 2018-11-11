from django.test import TestCase
from behave import given, when, then

from api.engine.models import Dormitory, RoomCharacteristics, RadioFilter, Option

def create_meals():
    meals = RadioFilter(name='meals')
    meals.save()

    options = [Option(name='Breakfast'),
               Option(name='Dinner'),
               Option(name='Both')]
    
    for option in options:
        option.radio_filter = meals
        option.save()
        option = Option.objects.filter(name=option.name)

    meals = RadioFilter.objects.filter(name='meals').first()

    return meals

@given('we have 1 dormitory with 2 rooms')
def prepare_dormitory(self):
    self.alfam = Dormitory(name='Alfam')
    self.alfam.save()

    self.meals = create_meals()

    self.room1 = RoomCharacteristics(dormitory=self.alfam)
    self.room1.save()
    self.room1.filters.add(self.meals)
    self.room1.save()

    self.room2 = RoomCharacteristics(dormitory=self.alfam)
    self.room2.save()


@when('filtering alfam rooms by meal')
def filtering(self):
    filters = [self.meals.get_query(['Dinner',]), ]
    self.filtered_dorm_alfam = Dormitory.objects.apply_filters(filters)

@then('get alfam dormitory with just one room')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().room_characteristics.all().count() == 1