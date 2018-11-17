from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework import status

from behave import given, when, then

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
    pass


@when('hitting GET /filters endpoint in English')
def test_model_can_create_a_message(self):
    pass


@then('get 200 OK with English filters')
def filtering(self):
    pass


@when('hitting GET /filters endpoint in Turkish')
def test_model_can_create_a_message(self):
    pass


@then('get 200 OK with Turkish filters')
def filtering(self):
    pass


@when('hitting POST /dorms endpoint in English')
def filtering(self):
    pass


@then('get 200 OK with English rooms characteristics')
def filtering(self):
    pass


@when('hitting POST /dorms endpoint in Turkish')
def filtering(self):
    pass


@then('get 200 OK with Turkish rooms characteristics')
def filtering(self):
    pass


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
