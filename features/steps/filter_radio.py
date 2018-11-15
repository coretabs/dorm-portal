from behave import given, when, then

from api.engine.models import *

from features.steps.factory import *


@given('we have 1 dormitory with 2 rooms')
def prepare_dormitory(self):
    self.alfam = Dormitory(name='Alfam')
    self.alfam.save()

    self.options = [Option(name='Breakfast'),
                    Option(name='Dinner'),
                    Option(name='Both')]

    self.meals = create_radio_filter(self.options, 'meals')

    self.meals_choice1 = create_radio_choice(self.options[0], self.meals)
    self.room1 = create_room_with_radio_choices(self.alfam, [self.meals_choice1, ])

    self.meals_choice2 = create_radio_choice(self.options[1], self.meals)
    self.room2 = create_room_with_radio_choices(self.alfam, [self.meals_choice2, ])
    self.room3 = create_room_with_radio_choices(self.alfam, [self.meals_choice2, ])

    self.room4 = RoomCharacteristics(dormitory=self.alfam)
    self.room4.save()


@when('filtering alfam rooms by meal Breakfast')
def filtering(self):
    choosen_option_id = [self.meals_choice1.selected_option.id, ]
    filters = [self.meals.get_query(choosen_option_id), ]
    self.filtered_dorm_alfam = Dormitory.objects.apply_room_filters(filters)


@then('get alfam dormitory with just one room having Breakfast')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().room_characteristics.all().count() == 1
    assert self.filtered_dorm_alfam.first()\
        .room_characteristics.first()\
        .radio_choices.first().selected_option.name == 'Breakfast'


@when('filtering alfam rooms by meal Dinner')
def filtering(self):
    choosen_option_id = [self.meals_choice2.selected_option.id, ]
    filters = [self.meals.get_query(choosen_option_id), ]
    self.filtered_dorm_alfam = Dormitory.objects.apply_room_filters(filters)


@then('get alfam dormitory with just two room having Dinner')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().room_characteristics.all().count() == 2

    assert self.filtered_dorm_alfam.first()\
        .room_characteristics.all()[0]\
        .radio_choices.first().selected_option.name == 'Dinner'

    assert self.filtered_dorm_alfam.first()\
        .room_characteristics.all()[1]\
        .radio_choices.first().selected_option.name == 'Dinner'


@when('filtering alfam rooms by meal Breakfast & Dinner')
def filtering(self):
    choosen_option_ids = [self.meals_choice1.selected_option.id,
                          self.meals_choice2.selected_option.id]
    filters = [self.meals.get_query(choosen_option_ids), ]
    self.filtered_dorm_alfam = Dormitory.objects.apply_room_filters(filters)


@then('get dormitory with all room having Breakfast & Dinner')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm_alfam.first().room_characteristics.all().count() == 3

    assert self.filtered_dorm_alfam.first()\
        .room_characteristics.all()[0]\
        .radio_choices.first().selected_option.name == 'Breakfast'

    assert self.filtered_dorm_alfam.first()\
        .room_characteristics.all()[1]\
        .radio_choices.first().selected_option.name == 'Dinner'

    assert self.filtered_dorm_alfam.first()\
        .room_characteristics.all()[2]\
        .radio_choices.first().selected_option.name == 'Dinner'
