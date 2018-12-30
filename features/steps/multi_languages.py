from django.urls import reverse
from django.utils import translation

from rest_framework.test import APIRequestFactory
from rest_framework import status

from behave import given, when, then

from i18nfield.strings import LazyI18nString

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


@given('we have 3 langs En,Ar,Tr and 2 currencies USD,TL')
def arrange(context):
    context.languages = settings.LANGUAGES
    context.usd = create_currency('USD', '$')
    context.tl = create_currency('TL', '₺')


@when('serializing 3 langs En,Ar,Tr and 2 currencies USD,TL')
def act(context):
    context.serialized_locale = LocaleSerailizer([])
    context.serialized_locale_string = str(context.serialized_locale.data)


@then('get valid serialized languages and currencies')
def test(context):
    # print(context.serialized_locale.data)

    assert context.serialized_locale_string.count(
        "('name', 'Türkçe')") == 1


@when('hitting GET /locale endpoint')
def act(context):
    request = APIRequestFactory().get(reverse('engine:locale-list'))
    view = LocaleListViewSet.as_view(actions={'get': 'list'})
    context.response = view(request)


@then('get 200 OK with langs and currencies')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK

    languages_prices_keys = context.response.render().data.keys()
    number_of_returned_json_data = len(list(languages_prices_keys))
    # print(context.response.render().data)
    assert number_of_returned_json_data == 2


@given('we have 1 dorm with 2 rooms with meals and luxury shower')
def arrange(context):
    context.category_public = create_category(LazyI18nString(
        {'ar': 'عام', 'tr': 'Genel', 'en': 'Public'}))
    context.alfam = create_dorm('Alfam', context.category_public)

    context.luxury_shower = create_room_feature(LazyI18nString(
        {'ar': 'شاور فاخر', 'tr': 'lüks duş', 'en': 'Luxury Shower'}))

    context.room_type_options = [RadioOption(name=LazyI18nString(
        {'ar': 'غرفة سنجل', 'tr': 'tek oda', 'en': 'Single'})),
        RadioOption(name=LazyI18nString(
            {'ar': 'غرفة دبل', 'tr': 'double oda', 'en': 'Double'}))]
    context.room_types = create_radio_filter(context.room_type_options, LazyI18nString(
        {'ar': 'نوع الغرفة', 'tr': 'oda tip', 'en': 'Room Type'}))
    context.room_type_single_choice = create_radio_choice(
        context.room_type_options[0], context.room_types)
    context.room_type_double_choice = create_radio_choice(
        context.room_type_options[1], context.room_types)

    context.people_allowed_number_filter = IntegralFilter(name='People Allowed Number')
    context.people_allowed_number_filter.save()
    context.one_person = create_integral_choice(context.people_allowed_number_filter, 1)
    context.two_persons = create_integral_choice(context.people_allowed_number_filter, 2)

    context.meal_options = [
        RadioOption(name=LazyI18nString({'ar': 'افطار', 'tr': 'Kahvalti', 'en': 'Breakfast'})),
        RadioOption(name=LazyI18nString({'ar': 'عشاء', 'tr': 'Akşam Yemeği', 'en': 'Dinner'}))]
    context.meals = create_radio_filter(context.meal_options, name=LazyI18nString(
        {'ar': 'وجبة', 'tr': 'Yemek', 'en': 'Meals'}))
    context.meals_choice_breakfast = create_radio_choice(context.meal_options[0], context.meals)
    context.meals_choice_dinner = create_radio_choice(context.meal_options[1], context.meals)

    context.price_filter = IntegralFilter(name=LazyI18nString(
        {'ar': 'السعر', 'tr': 'Fiyat', 'en': 'Price'}))
    context.price_filter.save()
    context.price_1000 = create_integral_choice(context.price_filter, 1000)

    context.options_duration = [
        RadioOption(name=LazyI18nString({'ar': 'ربيع', 'tr': 'Ilkbahar', 'en': 'Spring'})),
        RadioOption(name=LazyI18nString({'ar': 'شتاء', 'tr': 'Kış', 'en': 'Winter'}))]
    context.duration = create_radio_filter(context.options_duration, LazyI18nString(
        {'ar': 'المدة', 'tr': 'Müddet', 'en': 'Duration'}))
    context.duration_choice_spring = create_radio_choice(
        context.options_duration[0], context.duration)
    context.duration_choice_winter = create_radio_choice(
        context.options_duration[1], context.duration)

    context.room1 = create_room_with_radio_integral_features(
        context.alfam,
        [context.meals_choice_dinner, context.room_type_single_choice, context.duration_choice_spring],
        [context.price_1000, context.one_person],
        [])

    context.room2 = create_room_with_radio_integral_features(
        context.alfam,
        [context.meals_choice_breakfast, context.room_type_double_choice, context.duration_choice_winter],
        [context.price_1000, context.two_persons],
        [context.luxury_shower, ])


@when('hitting GET /filters endpoint in English')
def act(context):
    translation.activate('en')

    request = APIRequestFactory().get(reverse('engine:filters-list'))
    view = FiltersListViewSet.as_view(actions={'get': 'list'})
    context.response = view(request)


@then('get 200 OK with English filters')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    # print(context.response.render().data)
    assert str(context.response.render().data).count("('name', 'Public')") == 1


@when('hitting GET /filters endpoint in Turkish')
def act(context):
    translation.activate('tr')

    request = APIRequestFactory().get(reverse('engine:filters-list'))
    view = FiltersListViewSet.as_view(actions={'get': 'list'})
    context.response = view(request)


@then('get 200 OK with Turkish filters')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    assert str(context.response.render().data).count("('name', 'Genel')") == 1


@when('hitting POST /dorms endpoint in English')
def act(context):
    translation.activate('en')

    request = APIRequestFactory().post(reverse('engine:dorms-list'), format='json')
    view = DormViewSet.as_view(actions={'post': 'create'})
    context.response = view(request)


@then('get 200 OK with English rooms characteristics')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK

    returned_dorms = context.response.render().data[0]

    number_of_returned_json_filters = len(list(returned_dorms))
    assert number_of_returned_json_filters == 11

    # print(context.response.render().data)
    assert str(context.response.render().data).count("('choice', 'Breakfast')") == 1


@when('hitting POST /dorms endpoint in Turkish')
def act(context):
    translation.activate('tr')

    request = APIRequestFactory().post(reverse('engine:dorms-list'), format='json')
    view = DormViewSet.as_view(actions={'post': 'create'})
    context.response = view(request)


@then('get 200 OK with Turkish rooms characteristics')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK

    returned_dorms = context.response.render().data[0]

    number_of_returned_json_filters = len(list(returned_dorms))
    assert number_of_returned_json_filters == 11

    # print(context.response.render().data)
    assert str(context.response.render().data).count("('choice', 'Kahvalti')") == 1
