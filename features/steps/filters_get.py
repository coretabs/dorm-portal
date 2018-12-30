from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework import status

from behave import given, when, then

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


@given('we have 2 dormitory with 3 prices and 3 meal options')
def arrange(context):

    category_public = create_category('public')
    context.alfam = create_dorm('Alfam', category_public)

    context.price_filter = IntegralFilter(name='Price')
    context.price_filter.save()

    context.price_alfam1 = create_integral_choice(context.price_filter, 1000)
    context.price_alfam2 = create_integral_choice(context.price_filter, 1200)
    context.price_alfam3 = create_integral_choice(context.price_filter, 1700)

    context.options = [RadioOption(name='Breakfast'),
                       RadioOption(name='Dinner'),
                       RadioOption(name='Both')]

    context.meals = create_radio_filter(context.options, 'Meals')

    context.meals_choice1 = create_radio_choice(context.options[0], context.meals)
    context.meals_choice2 = create_radio_choice(context.options[1], context.meals)


@when('adding main filters (duration)')
def act(context):
    context.options_duration = [RadioOption(name='Spring'),
                                RadioOption(name='Winter'),
                                RadioOption(name='Summer'),
                                RadioOption(name='Full year')]
    context.duration = create_radio_filter(context.options_duration, 'Duration')
    context.duration_choice = create_radio_choice(
        context.options_duration[0], context.duration)

    context.all_filters = ClientReturnedFiltersSerializer([])
    context.all_filters_string = str(context.all_filters.data)


@then('will get main filters (duration and category)')
def test(context):
    assert Filter.objects.filter(name__contains='Duration').count() == 1

    print(context.all_filters_string)

    assert context.all_filters_string.count("('name', 'Spring')") == 1
    assert context.all_filters_string.count("('name', 'public')") == 1


@when('getting additional_filters: prices and meals')
def act(context):
    context.all_filters = ClientReturnedFiltersSerializer([])
    context.all_filters_string = str(context.all_filters.data)


@then('get additional_filters: with price min_max and meals')
def test(context):
    assert Filter.objects.additional_filters().count() == 2

    assert context.all_filters_string.count(
        "('name', 'Meals'), ('is_checkbox', True), ('is_integral', False),") == 1

    assert context.all_filters_string.count(
        "('name', 'Price'), ('is_checkbox', False), ('is_integral', True), ('is_optional', True), ('value', [1000, 1700])") == 1


@when('having more than one integral filter (bathrooms)')
def act(context):
    context.bathrooms = IntegralFilter(name='bathroom')
    context.bathrooms.save()
    context.bathrooms_alfam1 = create_integral_choice(context.bathrooms, 1)
    context.bathrooms_alfam2 = create_integral_choice(context.bathrooms, 2)
    context.all_filters = ClientReturnedFiltersSerializer([])
    context.all_filters_string = str(context.all_filters.data)


@then('will get bathrooms with the max bathrooms number correctly')
def test(context):
    assert Filter.objects.additional_filters().count() == 3

    assert context.all_filters_string.count(
        "('name', 'Meals'), ('is_checkbox', True), ('is_integral', False),") == 1

    assert context.all_filters_string.count(
        "('name', 'Price'), ('is_checkbox', False), ('is_integral', True), ('is_optional', True), ('value', [1000, 1700])") == 1


@then('not get main filters with the additional filters')
def test(context):
    additional_filters = Filter.objects.additional_filters()
    assert additional_filters.count() == 3

    assert additional_filters.filter(name='Duration').count() == 0


@when('adding features filters for dorms and rooms')
def act(context):
    context.swimming_pool = create_dorm_feature('Swimming pool')
    context.free_wifi = create_dorm_feature('Free WiFi')
    context.free_wifi = create_dorm_feature('Reception')

    context.luxury_shower = create_room_feature('Luxury shower')
    context.air_conditioner = create_room_feature('Air Conditioner')

    context.all_filters = ClientReturnedFiltersSerializer([])
    context.all_filters_string = str(context.all_filters.data)


@then('got both features filters for dorms and room')
def test(context):
    assert Filter.objects.dorm_features().count() == 3
    assert Filter.objects.room_features().count() == 2

    assert context.all_filters_string.count("('name', 'Swimming pool')") == 1
    assert context.all_filters_string.count("('name', 'Free WiFi')") == 1
    assert context.all_filters_string.count("('name', 'Reception')") == 1
    assert context.all_filters_string.count("('name', 'Luxury shower')") == 1
    assert context.all_filters_string.count("('name', 'Air Conditioner')") == 1


@when('requesting GET /filters')
def act(context):
    request = APIRequestFactory().get(reverse('engine:filters-list'))
    view = FiltersListViewSet.as_view(actions={'get': 'list'})
    context.response = view(request)


@then('get 200 OK and all filters in GET /filters')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK

    filters_keys = context.response.render().data.keys()
    number_of_returned_json_filters = len(list(filters_keys))
    print(context.response.render().data)
    assert number_of_returned_json_filters == 5
