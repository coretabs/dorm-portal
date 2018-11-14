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
    self.all_filters = FiltersSerializer([1, ], many=True)


@then('get additional_filters: with price min_max and meals')
def test_model_can_create_a_message(self):
    assert Filter.objects.count() == 2

    assert "('name', 'meals'), ('is_checkbox', True), ('is_integral', False)," in str(
        self.all_filters.data)

    assert "('name', 'price'), ('is_checkbox', False), ('is_integral', True), ('value', {'selected_number__max': 1700, 'selected_number__min': 1000})" in str(
        self.all_filters.data)


@when('having more than one integral filter (bathrooms)')
def prepare_dormitory(self):
    self.bathrooms = IntegralFilter(name='bathroom')
    self.bathrooms.save()
    self.bathrooms_alfam1 = create_integral_choice(self.bathrooms, 1)
    self.bathrooms_alfam2 = create_integral_choice(self.bathrooms, 2)
    self.all_filters = FiltersSerializer([1, ], many=True)


@then('will get bathrooms with the max bathrooms number correctly')
def test_model_can_create_a_message(self):
    assert Filter.objects.count() == 3

    assert "('name', 'meals'), ('is_checkbox', True), ('is_integral', False)," in str(
        self.all_filters.data)

    assert "('name', 'price'), ('is_checkbox', False), ('is_integral', True), ('value', {'selected_number__max': 1700, 'selected_number__min': 1000})" in str(
        self.all_filters.data)


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

    self.all_filters = FiltersSerializer([1, ], many=True)


@then('will get main filters (category and academic year)')
def test_model_can_create_a_message(self):
    assert Filter.objects.main_filters().count() == 2

    assert "('name', 'academic year'), ('is_checkbox', True), ('is_integral', False)," in str(
        self.all_filters.data)

    assert "('name', 'category'), ('is_checkbox', True), ('is_integral', False)," in str(
        self.all_filters.data)


@then('not get main filters with the additional filters')
def test_model_can_create_a_message(self):
    additional_filters = (Filter.objects.radio_filters() |
                          Filter.objects.integral_filters()).distinct()
    assert additional_filters.count() == 3

    assert additional_filters.filter(name='category').count() == 0
    assert additional_filters.filter(name='academic year').count() == 0
