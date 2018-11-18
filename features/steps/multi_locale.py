from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework import status

from behave import given, when, then

from i18nfield.strings import LazyI18nString

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


def create_currency(code, symbol):
    result = Currency(code=code, symbol=symbol)
    result.save()

    return result


@given('we have 3 langs En,Ar,Tr and 2 currencies USD,TL')
def prepare_dormitory(self):
    self.languages = settings.LANGUAGES
    self.usd = create_currency('USD', '$')
    self.tl = create_currency('TL', '₺')


@when('serializing 3 langs En,Ar,Tr and 2 currencies USD,TL')
def filtering(self):
    self.serialized_locale = LocaleSerailizer([])
    self.serialized_locale_string = str(self.serialized_locale.data)


@then('get valid serialized languages and currencies')
def test_model_can_create_a_message(self):
    # print(self.serialized_locale.data)

    assert self.serialized_locale_string.count(
        "('name', 'Türkçe')") == 1


@when('hitting GET /locale endpoint')
def filtering(self):
    request = APIRequestFactory().get(reverse('locale-list'))
    view = LocaleListViewSet.as_view(actions={'get': 'list'})
    self.response = view(request)


@then('get 200 OK with langs and currencies')
def test_model_can_create_a_message(self):
    assert self.response.status_code == status.HTTP_200_OK

    languages_prices_keys = self.response.render().data.keys()
    number_of_returned_json_data = len(list(languages_prices_keys))
    # print(self.response.render().data)
    assert number_of_returned_json_data == 2


@given('we have 1 dorm with 2 rooms with meals and luxury shower')
def filtering(self):
    self.category_public = create_category(LazyI18nString(
        {'ar': 'عام', 'tr': 'Genel', 'en': 'Public'}))
    self.alfam = create_dorm('Alfam', self.category_public)

    self.luxury_shower = create_room_feature(LazyI18nString(
        {'ar': 'شاور فاخر', 'tr': 'lüks duş', 'en': 'Luxury Shower'}))

    self.meal_options = [
        RadioOption(name=LazyI18nString({'ar': 'افطار', 'tr': 'Kahvalti', 'en': 'Breakfast'})),
        RadioOption(name=LazyI18nString({'ar': 'عشاء', 'tr': 'Akşam Yemeği', 'en': 'Dinner'}))]
    self.meals = create_radio_filter(self.meal_options, name=LazyI18nString(
        {'ar': 'وجبة', 'tr': 'Yemek', 'en': 'Meals'}))
    self.meals_choice_breakfast = create_radio_choice(self.meal_options[0], self.meals)
    self.meals_choice_dinner = create_radio_choice(self.meal_options[1], self.meals)

    self.price_filter = IntegralFilter(name=LazyI18nString(
        {'ar': 'السعر', 'tr': 'Fiyat', 'en': 'Price'}))
    self.price_filter.save()
    self.price_1000 = create_integral_choice(self.price_filter, 1000)

    self.options_duration = [
        RadioOption(name=LazyI18nString({'ar': 'ربيع', 'tr': 'Ilkbahar', 'en': 'Spring'})),
        RadioOption(name=LazyI18nString({'ar': 'شتاء', 'tr': 'Kış', 'en': 'Winter'}))]
    self.duration = create_radio_filter(self.options_duration, LazyI18nString(
        {'ar': 'المدة', 'tr': 'Müddet', 'en': 'Duration'}))

    self.room1 = create_room_with_radio_integral_features(
        self.alfam,
        [self.meals_choice_dinner, ],
        [self.price_1000, ],
        [])

    self.room2 = create_room_with_radio_integral_features(
        self.alfam,
        [self.meals_choice_breakfast, ],
        [self.price_1000, ],
        [self.luxury_shower, ])


@when('hitting GET /filters endpoint in English')
def test_model_can_create_a_message(self):
    request = APIRequestFactory().get(reverse('filters-list'), {'language': 'en'})
    view = FiltersListViewSet.as_view(actions={'get': 'list'})
    self.response = view(request)


@then('get 200 OK with English filters')
def filtering(self):
    assert self.response.status_code == status.HTTP_200_OK
    # print(self.response.render().data)
    assert str(self.response.render().data).count("('name', 'Public')") == 1


@when('hitting GET /filters endpoint in Turkish')
def test_model_can_create_a_message(self):
    request = APIRequestFactory().get(reverse('filters-list'), {'language': 'tr'})
    view = FiltersListViewSet.as_view(actions={'get': 'list'})
    self.response = view(request)


@then('get 200 OK with Turkish filters')
def filtering(self):
    assert self.response.status_code == status.HTTP_200_OK
    assert str(self.response.render().data).count("('name', 'Genel')") == 1


@when('hitting POST /dorms endpoint in English')
def filtering(self):
    request = APIRequestFactory().post(reverse('dorms-list'), {'language': 'en'}, format='json')
    view = DormViewSet.as_view(actions={'post': 'list'})
    self.response = view(request)


@then('get 200 OK with English rooms characteristics')
def filtering(self):
    assert self.response.status_code == status.HTTP_200_OK

    returned_dorms = self.response.render().data[0]

    number_of_returned_json_filters = len(list(returned_dorms))
    assert number_of_returned_json_filters == 4

    # print(self.response.render().data)
    assert str(self.response.render().data).count("('choice', 'Breakfast')") == 1


@when('hitting POST /dorms endpoint in Turkish')
def filtering(self):
    request = APIRequestFactory().post(reverse('dorms-list'), {'language': 'tr'}, format='json')
    view = DormViewSet.as_view(actions={'post': 'list'})
    self.response = view(request)


@then('get 200 OK with Turkish rooms characteristics')
def filtering(self):
    assert self.response.status_code == status.HTTP_200_OK

    returned_dorms = self.response.render().data[0]

    number_of_returned_json_filters = len(list(returned_dorms))
    assert number_of_returned_json_filters == 4

    # print(self.response.render().data)
    assert str(self.response.render().data).count("('choice', 'Kahvalti')") == 1


@when('querying dorms with TL')
def test_model_can_create_a_message(self):
    pass


@then('getting price in TL')
def filtering(self):
    pass


@when('hitting POST /dorms endpoint in TL')
def test_model_can_create_a_message(self):
    pass


@then('get 200 OK with TL prices')
def filtering(self):
    pass
