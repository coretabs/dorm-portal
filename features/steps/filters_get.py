from django.test import TestCase
from behave import given, when, then

from api.engine.models import *
from api.engine.serializers import *

from features.steps.factory import *


@given('we have 2 dormitory with 3 prices and 3 meal options')
def prepare_dormitory(self):
    self.alfam = Dormitory(name='Alfam')
    self.alfam.save()

    self.integral_filter = IntegralFilter(name='price')
    self.integral_filter.save()

    self.price_alfam1 = create_integral_choice(self.integral_filter, 1000)
    self.price_alfam2 = create_integral_choice(self.integral_filter, 1200)
    self.price_alfam3 = create_integral_choice(self.integral_filter, 1700)

    self.options = [Option(name='Breakfast'),
                    Option(name='Dinner'),
                    Option(name='Both')]

    self.meals = create_radio_filter(self.options, 'meals')

    self.meals_choice1 = create_radio_choice(self.options[0], self.meals)
    self.meals_choice2 = create_radio_choice(self.options[1], self.meals)


@when('getting additional_filters: prices and meals')
def filtering(self):
    self.all_filters = FiltersSerializer([])
    self.all_filters_string = str(self.all_filters.data)


@then('get additional_filters: with price min_max and meals')
def test_model_can_create_a_message(self):
    assert Filter.objects.additional_filters().count() == 2

    assert self.all_filters_string.count(
        "('name', 'meals'), ('is_checkbox', True), ('is_integral', False),") == 1

    assert self.all_filters_string.count(
        "('name', 'price'), ('is_checkbox', False), ('is_integral', True), ('value', {'selected_number__max': 1700, 'selected_number__min': 1000})") == 1


@when('having more than one integral filter (bathrooms)')
def prepare_dormitory(self):
    self.bathrooms = IntegralFilter(name='bathroom')
    self.bathrooms.save()
    self.bathrooms_alfam1 = create_integral_choice(self.bathrooms, 1)
    self.bathrooms_alfam2 = create_integral_choice(self.bathrooms, 2)
    self.all_filters = FiltersSerializer([])
    self.all_filters_string = str(self.all_filters.data)


@then('will get bathrooms with the max bathrooms number correctly')
def test_model_can_create_a_message(self):
    assert Filter.objects.additional_filters().count() == 3

    assert self.all_filters_string.count(
        "('name', 'meals'), ('is_checkbox', True), ('is_integral', False),") == 1

    assert self.all_filters_string.count(
        "('name', 'price'), ('is_checkbox', False), ('is_integral', True), ('value', {'selected_number__max': 1700, 'selected_number__min': 1000})") == 1


@when('adding main filters (category and academic year)')
def prepare_dormitory(self):
    self.options_category = [Option(name='Public'),
                             Option(name='Private'),
                             Option(name='Both')]
    self.category = create_radio_filter(self.options_category, 'category')
    self.category_choice = create_radio_choice(
        self.options_category[0], self.category)

    self.options_academic_year = [Option(name='Spring'),
                                  Option(name='Winter'),
                                  Option(name='Summer'),
                                  Option(name='Full year')]
    self.academic_year = create_radio_filter(self.options_academic_year, 'academic year')
    self.academic_year_choice = create_radio_choice(
        self.options_academic_year[0], self.academic_year)

    self.all_filters = FiltersSerializer([])
    self.all_filters_string = str(self.all_filters.data)


@then('will get main filters (category and academic year)')
def test_model_can_create_a_message(self):
    assert Filter.objects.main_filters().count() == 2

    assert self.all_filters_string.count(
        "('name', 'academic year'), ('is_checkbox', True), ('is_integral', False),") == 1

    assert self.all_filters_string.count(
        "('name', 'category'), ('is_checkbox', True), ('is_integral', False),") == 1


@then('not get main filters with the additional filters')
def test_model_can_create_a_message(self):
    additional_filters = Filter.objects.additional_filters()
    assert additional_filters.count() == 3

    assert additional_filters.filter(name='category').count() == 0
    assert additional_filters.filter(name='academic year').count() == 0


@when('adding features filters for dorms and rooms')
def prepare_features(self):
    self.swimming_pool = create_dorm_feature('Swimming pool')
    self.free_wifi = create_dorm_feature('Free WiFi')
    self.free_wifi = create_dorm_feature('Reception')

    self.luxury_shower = create_room_feature('Luxury shower')
    self.air_conditioner = create_room_feature('Air Conditioner')

    self.all_filters = FiltersSerializer([])
    self.all_filters_string = str(self.all_filters.data)


@then('got both features filters for dorms and room')
def test_model_can_create_a_message(self):
    assert Filter.objects.dorm_features().count() == 3
    assert Filter.objects.room_features().count() == 2

    assert self.all_filters_string.count("('name', 'Swimming pool')") == 1
    assert self.all_filters_string.count("('name', 'Free WiFi')") == 1
    assert self.all_filters_string.count("('name', 'Reception')") == 1
    assert self.all_filters_string.count("('name', 'Luxury shower')") == 1
    assert self.all_filters_string.count("('name', 'Air Conditioner')") == 1
