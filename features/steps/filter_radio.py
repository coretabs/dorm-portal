from django.test import TestCase
from behave import given, when, then

from api.engine.models import Dormitory, RoomCharacteristics, RadioChoice, RadioFilter, Option

def create_meals(self):
    meals = RadioChoice(name='meals')
    meals.save()

    self.options = [Option(name='Breakfast'),
               Option(name='Dinner'),
               Option(name='Both')]
    
    for option in self.options:
        option.radio_choice = meals
        option.save()
        option = Option.objects.filter(name=option.name)

    meals = RadioChoice.objects.filter(name='meals').first()

    return meals

@given('we have 1 dormitory with 2 rooms')
def prepare_dormitory(self):
    self.alfam = Dormitory(name='Alfam')
    self.alfam.save()

    self.meals = create_meals(self)
    self.meals_filter1 = RadioFilter()
    self.meals_filter1.selected_option = self.options[0]
    self.meals_filter1.radio_choice = self.meals
    self.meals_filter1.save()
    self.meals_filter1 = RadioFilter.objects.get(pk=1)

    self.room1 = RoomCharacteristics(dormitory=self.alfam)
    self.room1.save()
    self.room1.filters.add(self.meals_filter1)
    self.room1.save()

    self.meals = create_meals(self)
    self.meals_filter2 = RadioFilter()
    self.meals_filter2.selected_option = self.options[1]
    self.meals_filter2.radio_choice = self.meals
    self.meals_filter2.save()
    self.meals_filter2 = RadioFilter.objects.get(pk=2)

    self.room2 = RoomCharacteristics(dormitory=self.alfam)
    self.room2.save()
    self.room2.filters.add(self.meals_filter2)
    self.room2.save()

    self.room3 = RoomCharacteristics(dormitory=self.alfam)
    self.room3.save()
    self.room3.filters.add(self.meals_filter2)
    self.room3.save()

    self.room4 = RoomCharacteristics(dormitory=self.alfam)
    self.room4.save()


@when('filtering alfam rooms by meal Breakfast')
def filtering(self):
    choosen_option_id = self.meals_filter1.selected_option.id
    filters = [self.meals_filter1.get_query([choosen_option_id,]), ]
    #breakpoint()
    self.filtered_dorm_alfam = Dormitory.objects.apply_room_filters(filters)


@then('get alfam dormitory with just one room having Breakfast')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().room_characteristics.all().count() == 1
    assert self.filtered_dorm_alfam.first()\
                        .room_characteristics.first()\
                        .filters.first().selected_option.name == 'Breakfast'

    
@when('filtering alfam rooms by meal Dinner')
def filtering(self):
    choosen_option_id = self.meals_filter2.selected_option.id
    filters = [self.meals_filter2.get_query([choosen_option_id,]), ]
    self.filtered_dorm_alfam = Dormitory.objects.apply_room_filters(filters)


@then('get alfam dormitory with just two room having Dinner')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().room_characteristics.all().count() == 2

    assert self.filtered_dorm_alfam.first()\
                        .room_characteristics.all()[0]\
                        .filters.first().selected_option.name == 'Dinner'

    assert self.filtered_dorm_alfam.first()\
                        .room_characteristics.all()[1]\
                        .filters.first().selected_option.name == 'Dinner'


@when('filtering alfam rooms by meal Breakfast & Dinner')
def filtering(self):
    choosen_option_ids = [self.meals_filter1.selected_option.id,
                          self.meals_filter2.selected_option.id]
    filters = [self.meals_filter2.get_query(choosen_option_ids), ]
    self.filtered_dorm_alfam = Dormitory.objects.apply_room_filters(filters)


@then('get dormitory with all room having Breakfast & Dinner')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().room_characteristics.all().count() == 3

    assert self.filtered_dorm_alfam.first()\
                        .room_characteristics.all()[0]\
                        .filters.first().selected_option.name == 'Breakfast'

    assert self.filtered_dorm_alfam.first()\
                        .room_characteristics.all()[1]\
                        .filters.first().selected_option.name == 'Dinner'

    assert self.filtered_dorm_alfam.first()\
                        .room_characteristics.all()[2]\
                        .filters.first().selected_option.name == 'Dinner'