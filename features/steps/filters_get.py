from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework import status

from behave import given, when, then

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


@given('we have 2 dormitory with 3 prices and 3 meal options')
def prepare_dormitory(self):

    category_public = create_category('public')
    self.alfam = create_dorm('Alfam', category_public)

    self.price_filter = IntegralFilter(name='Price')
    self.price_filter.save()

    self.price_alfam1 = create_integral_choice(self.price_filter, 1000)
    self.price_alfam2 = create_integral_choice(self.price_filter, 1200)
    self.price_alfam3 = create_integral_choice(self.price_filter, 1700)

    self.options = [RadioOption(name='Breakfast'),
                    RadioOption(name='Dinner'),
                    RadioOption(name='Both')]

    self.meals = create_radio_filter(self.options, 'Meals')

    self.meals_choice1 = create_radio_choice(self.options[0], self.meals)
    self.meals_choice2 = create_radio_choice(self.options[1], self.meals)


@when('adding main filters (duration)')
def prepare_dormitory(self):
    self.options_duration = [RadioOption(name='Spring'),
                             RadioOption(name='Winter'),
                             RadioOption(name='Summer'),
                             RadioOption(name='Full year')]
    self.duration = create_radio_filter(self.options_duration, 'Duration')
    self.duration_choice = create_radio_choice(
        self.options_duration[0], self.duration)

    self.all_filters = ClientReturnedFiltersSerializer([])
    self.all_filters_string = str(self.all_filters.data)


@then('will get main filters (duration and category)')
def test_model_can_create_a_message(self):
    assert Filter.objects.main_filters().count() == 1

    print(self.all_filters_string)

    assert self.all_filters_string.count("('name', 'Spring')") == 1
    assert self.all_filters_string.count("('name', 'public')") == 1


@when('getting additional_filters: prices and meals')
def filtering(self):
    self.all_filters = ClientReturnedFiltersSerializer([])
    self.all_filters_string = str(self.all_filters.data)


@then('get additional_filters: with price min_max and meals')
def test_model_can_create_a_message(self):
    assert Filter.objects.additional_filters().count() == 2

    assert self.all_filters_string.count(
        "('name', 'Meals'), ('is_checkbox', True), ('is_integral', False),") == 1

    assert self.all_filters_string.count(
        "('name', 'Price'), ('is_checkbox', False), ('is_integral', True), ('value', {'selected_number__max': 1700, 'selected_number__min': 1000})") == 1


@when('having more than one integral filter (bathrooms)')
def prepare_dormitory(self):
    self.bathrooms = IntegralFilter(name='bathroom')
    self.bathrooms.save()
    self.bathrooms_alfam1 = create_integral_choice(self.bathrooms, 1)
    self.bathrooms_alfam2 = create_integral_choice(self.bathrooms, 2)
    self.all_filters = ClientReturnedFiltersSerializer([])
    self.all_filters_string = str(self.all_filters.data)


@then('will get bathrooms with the max bathrooms number correctly')
def test_model_can_create_a_message(self):
    assert Filter.objects.additional_filters().count() == 3

    assert self.all_filters_string.count(
        "('name', 'Meals'), ('is_checkbox', True), ('is_integral', False),") == 1

    assert self.all_filters_string.count(
        "('name', 'Price'), ('is_checkbox', False), ('is_integral', True), ('value', {'selected_number__max': 1700, 'selected_number__min': 1000})") == 1


@then('not get main filters with the additional filters')
def test_model_can_create_a_message(self):
    additional_filters = Filter.objects.additional_filters()
    assert additional_filters.count() == 3

    assert additional_filters.filter(name='Duration').count() == 0


@when('adding features filters for dorms and rooms')
def prepare_features(self):
    self.swimming_pool = create_dorm_feature('Swimming pool')
    self.free_wifi = create_dorm_feature('Free WiFi')
    self.free_wifi = create_dorm_feature('Reception')

    self.luxury_shower = create_room_feature('Luxury shower')
    self.air_conditioner = create_room_feature('Air Conditioner')

    self.all_filters = ClientReturnedFiltersSerializer([])
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


@when('requesting GET /filters')
def prepare_features(self):
    request = APIRequestFactory().get(reverse('engine:filters-list'))
    view = FiltersListViewSet.as_view(actions={'get': 'list'})
    self.response = view(request)


@then('get 200 OK and all filters in GET /filters')
def test_model_can_create_a_message(self):
    assert self.response.status_code == status.HTTP_200_OK

    filters_keys = self.response.render().data.keys()
    number_of_returned_json_filters = len(list(filters_keys))
    print(self.response.render().data)
    assert number_of_returned_json_filters == 5
