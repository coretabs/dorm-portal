import decimal

from django.test import TestCase
from django.core.management import call_command
from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework import status

from behave import given, when, then

from features.steps.factory import *

from djmoney.contrib.exchange.models import *

from api.engine import exchange_backends

from api.engine.views import *
from api.engine.serializers import *


@given('we have all exchange rates')
def arrange(context):
    assert Rate.objects.count() == 0
    call_command('update_rates')
    assert Rate.objects.count() > 0


@given('two rooms price currencies are in USD and one in TRY and one in EUR')
def arrange(context):
    try_currency = create_currency('₺', 'TRY')
    eur_currency = create_currency('€', 'EUR')

    # context.room1 already usd
    # context.room2 already usd
    context.room3.price_currency = try_currency
    context.room4.price_currency = eur_currency
    context.room3.save()
    context.room4.save()


@given('the rate to TRY is 5 and rate for EUR is 0.5')
def arrange(context):
    try_rate = Rate.objects.get(currency='TRY')
    eur_rate = Rate.objects.get(currency='EUR')
    try_rate.value = 5.0
    eur_rate.value = 0.5
    try_rate.save()
    eur_rate.save()


@when('get dorms with USD currency')
def act(context):
    context.filtered_dorms = Dormitory.objects.apply_room_filters([], to_currency='USD')


@then('get all rooms in USD')
def test(context):
    assert context.filtered_dorms[0].room_characteristics.all()[0].price == 1000
    assert context.filtered_dorms[0].room_characteristics.all()[1].price == 1200
    assert context.filtered_dorms[1].room_characteristics.all()[0].price == 1700 / 5
    assert context.filtered_dorms[1].room_characteristics.all()[1].price == 2000 * 2


@when('get dorms with TRY currency')
def act(context):
    context.filtered_dorms = Dormitory.objects.apply_room_filters([], to_currency='TRY')


@then('get all rooms in TRY')
def test(context):
    assert context.filtered_dorms[0].room_characteristics.all()[0].price == 5000
    assert context.filtered_dorms[0].room_characteristics.all()[1].price == 6000
    assert context.filtered_dorms[1].room_characteristics.all()[0].price == 1700
    assert context.filtered_dorms[1].room_characteristics.all()[1].price == 2000 * 2 * 5


@when('get dorms with EUR currency')
def act(context):
    context.filtered_dorms = Dormitory.objects.apply_room_filters([], to_currency='EUR')


@then('get all rooms in EUR')
def test(context):
    assert context.filtered_dorms[0].room_characteristics.all()[0].price == 1000 / 2
    assert context.filtered_dorms[0].room_characteristics.all()[1].price == 1200 / 2
    assert context.filtered_dorms[1].room_characteristics.all()[0].price == 1700 / 5 / 2
    assert context.filtered_dorms[1].room_characteristics.all()[1].price == 2000


@when('filtering rooms price with USD currency between 300 and 1500')
def act(context):
    filters = [context.price_filter.get_query(300, 1500), ]
    context.filtered_dorms = Dormitory.objects.apply_room_filters(filters, to_currency='USD')


@then('get three filtered rooms in USD (340 & 1000 & 1200)')
def test(context):
    assert context.filtered_dorms[0].room_characteristics.filter(price_converted=1000).count() == 1
    assert context.filtered_dorms[0].room_characteristics.filter(price_converted=1200).count() == 1
    assert context.filtered_dorms[1].room_characteristics.filter(price_converted=340).count() == 1


@when('filtering rooms price with TRY currency between 1500 and 5100')
def act(context):
    filters = [context.price_filter.get_query(1500, 5100), ]
    context.filtered_dorms = Dormitory.objects.apply_room_filters(filters, to_currency='TRY')


@then('get two filtered rooms in TRY (1700 & 5000)')
def test(context):
    assert context.filtered_dorms[0].room_characteristics.filter(price_converted=5000).count() == 1
    assert context.filtered_dorms[1].room_characteristics.filter(price_converted=1700).count() == 1


@when('filtering rooms price with EUR currency between 500 and 2000')
def act(context):
    filters = [context.price_filter.get_query(500, 2000), ]
    context.filtered_dorms = Dormitory.objects.apply_room_filters(filters, to_currency='EUR')


@then('get three filtered rooms in EUR (500 & 600 & 2000)')
def test(context):
    assert context.filtered_dorms[0].room_characteristics.filter(price_converted=500).count() == 1
    assert context.filtered_dorms[0].room_characteristics.filter(price_converted=600).count() == 1
    assert context.filtered_dorms[1].room_characteristics.filter(price_converted=2000).count() == 1


@when('serializing min_value max_value for price in USD')
def act(context):
    context.serialized_price = IntegralFilterSerializer(
        context.price_filter, context={'to_currency': 'USD'})
    context.serialized_price_string = str(context.serialized_price.data)


@then('get min_value=340 and max_value=4000 for USD')
def test(context):
    print(context.serialized_price_string)
    assert context.serialized_price_string.count("'value': [340, 4000],") == 1


@when('serializing min_value max_value for price in TRY')
def act(context):
    context.serialized_price = IntegralFilterSerializer(
        context.price_filter, context={'to_currency': 'TRY'})
    context.serialized_price_string = str(context.serialized_price.data)


@then('get min_value=1700 and max_value=20000 for TRY')
def test(context):
    print(context.serialized_price_string)
    assert context.serialized_price_string.count("'value': [1700, 20000],") == 1


@when('serializing min_value max_value for price in EUR')
def act(context):
    context.serialized_price = IntegralFilterSerializer(
        context.price_filter, context={'to_currency': 'EUR'})
    context.serialized_price_string = str(context.serialized_price.data)


@then('get min_value=170 and max_value=2000 for EUR')
def test(context):
    print(context.serialized_price_string)
    assert context.serialized_price_string.count("'value': [170, 2000],") == 1


@when('hitting POST /dorms endpoint in USD')
def act(context):
    request = APIRequestFactory().post(reverse('engine:dorms-list'),
                                       {'currency': 'USD'}, format='json')
    view = DormViewSet.as_view(actions={'post': 'create'})
    context.response = view(request)


@then('get 200 OK with USD prices')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    print(context.response.render().data)
    assert str(context.response.render().data).count("'price', 1200") == 1


@when('hitting POST /dorms endpoint in TRY')
def act(context):
    request = APIRequestFactory().post(reverse('engine:dorms-list'),
                                       {'currency': 'TRY'}, format='json')
    view = DormViewSet.as_view(actions={'post': 'create'})
    context.response = view(request)


@then('get 200 OK with TRY prices')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    print(context.response.render().data)
    assert str(context.response.render().data).count("'price', 5000") == 1


@when('hitting POST /dorms endpoint in EUR')
def act(context):
    request = APIRequestFactory().post(reverse('engine:dorms-list'),
                                       {'currency': 'EUR'}, format='json')
    view = DormViewSet.as_view(actions={'post': 'create'})
    context.response = view(request)


@then('get 200 OK with EUR prices')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    print(context.response.render().data)
    assert str(context.response.render().data).count("'price', 2000") == 1


@when('hitting POST /dorms endpoint in non registered currency')
def act(context):
    request = APIRequestFactory().post(reverse('engine:dorms-list'),
                                       {'currency': 'BlaBla'}, format='json')
    view = DormViewSet.as_view(actions={'post': 'create'})
    context.response = view(request)


@then('get 200 OK with default price currency (USD)')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    print(context.response.render().data)
    assert str(context.response.render().data).count("'price', 1200") == 1
