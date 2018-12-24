from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework import status

from behave import given, when, then

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


@given('we have 2 dormitory with 4 rooms with couple of choices')
def arrange(context):
    create_alfam_dovec_with_4_rooms(context)


@when('not doing any filtering for the dorms')
def act(context):
    context.filtered_dorms = Dormitory.objects.superfilter()


@then('get the 2 dorms with the 4 rooms')
def test(context):
    assert context.filtered_dorms.count() == 2
    assert context.filtered_dorms.all()[0].room_characteristics.count() == 2
    assert context.filtered_dorms.all()[1].room_characteristics.count() == 2


@then('get the rooms left equals the sum quota')
def test(context):
    assert context.filtered_dorms.count() == 2
    assert context.filtered_dorms.all()[0].rooms_left_in_dorm == 10
    assert context.filtered_dorms.all()[1].rooms_left_in_dorm == 10


@when('one of the alfam rooms has no quota')
def act(context):
    context.room1.allowed_quota = 0
    context.room1.save()
    context.filtered_dorms = Dormitory.objects.superfilter()


@then('get all the room except the one with no quota')
def test(context):
    assert context.filtered_dorms.count() == 2
    assert context.filtered_dorms.all()[0].room_characteristics.count() == 1
    assert context.filtered_dorms.all()[1].room_characteristics.count() == 2


@then('return the quota back for the alfam room')
def test(context):
    context.room1.allowed_quota = 5
    context.room1.save()


@when('filter free wifi')
def act(context):
    context.filtered_dorms = Dormitory.objects.superfilter(
        dorm_features_ids=[context.free_wifi.id, ])


@then('get only dovec which has free wifi with two rooms')
def test(context):
    assert context.filtered_dorms.count() == 1
    assert context.filtered_dorms.first().name == 'Dovec'
    assert context.filtered_dorms.all()[0].room_characteristics.count() == 2


@when('filter price between 1100 and 1800')
def act(context):
    price_choice = {'id': context.price_filter.id, 'min_value': 1100, 'max_value': 1800}
    context.filtered_dorms = Dormitory.objects.superfilter(radio_integeral_choices=[price_choice, ])


@then('get 2 dorms with 1 room for each (1200, 1700)')
def test(context):
    assert context.filtered_dorms.count() == 2
    assert context.filtered_dorms.all()[0].room_characteristics.count() == 1
    assert context.filtered_dorms.all()[1].room_characteristics.count() == 1


@when('filter PUBLIC dorm price between 1100 and 1800')
def act(context):
    price_choice = {'id': context.price_filter.id, 'min_value': 1100, 'max_value': 1800}
    context.filtered_dorms = Dormitory.objects.superfilter(category_id=context.category_public.id,
                                                           radio_integeral_choices=[price_choice, ])


@then('get alfam dorm with just 1 room (1200)')
def test(context):
    assert context.filtered_dorms.count() == 1
    assert context.filtered_dorms.first().name == 'Alfam'

    assert context.filtered_dorms.all()[0].room_characteristics.count() == 1
    assert context.filtered_dorms.all()[0].room_characteristics.first().price == 1200


@when('filter meals (breakfast & both) + luxury shower')
def act(context):
    breakfast_both = {'id': context.meals.id, 'choosen_options_ids': [
        context.meals_choice_breakfast.selected_option.id, context.meals_choice_both.selected_option.id]}

    context.filtered_dorms = Dormitory.objects.superfilter(
        radio_integeral_choices=[breakfast_both, ],
        room_features_ids=[context.luxury_shower.id, ])


@then('get only dovec with two rooms')
def test(context):
    assert context.filtered_dorms.count() == 1
    assert context.filtered_dorms.first().name == 'Dovec'
    assert context.filtered_dorms.all()[0].room_characteristics.count() == 2


@when('filter meals (without any option sent)')
def act(context):
    breakfast_both = {'id': context.meals.id, 'choosen_options_ids': []}

    context.filtered_dorms = Dormitory.objects.superfilter(
        radio_integeral_choices=[breakfast_both, ],)


@then('ignore the meals filter')
def test(context):
    assert context.filtered_dorms.count() == 2
    assert context.filtered_dorms.all()[0].room_characteristics.count() == 2
    assert context.filtered_dorms.all()[1].room_characteristics.count() == 2


@when('(breakfast&both) + luxuryshower + airconidtioner + price(1500,2000) + bathrooms(1,2)')
def act(context):
    price_choice = {'id': context.price_filter.id, 'min_value': 1500, 'max_value': 2000}
    bathroom_choice = {'id': context.bathrooms.id, 'min_value': 1, 'max_value': 2}

    breakfast_both = {'id': context.meals.id, 'choosen_options_ids': [
        context.meals_choice_breakfast.selected_option.id, context.meals_choice_both.selected_option.id]}

    context.filtered_dorms = Dormitory.objects.superfilter(
        radio_integeral_choices=[breakfast_both, price_choice, bathroom_choice],
        room_features_ids=[context.luxury_shower.id, context.air_conditioner.id])\
        .with_last_3_reviews().with_reviews_statistics()


@then('get only dovec with one room only')
def test(context):
    assert context.filtered_dorms.count() == 1
    assert context.filtered_dorms.first().name == 'Dovec'
    assert context.filtered_dorms.all()[0].room_characteristics.count() == 1


@when('deserialize the same filter above')
def act(context):
    price_choice = {'id': context.price_filter.id, 'min_value': 1500, 'max_value': 2000}
    bathroom_choice = {'id': context.bathrooms.id, 'min_value': 1, 'max_value': 2}
    breakfast_both = {'id': context.meals.id, 'choosen_options_ids': [
        context.meals_choice_breakfast.selected_option.id, context.meals_choice_both.selected_option.id]}

    context.same_filter_above_json = {'additional_filters': [price_choice, bathroom_choice, breakfast_both],
                                      'room_features': [context.luxury_shower.id, context.air_conditioner.id]}

    context.deserialized_data = ClientAcceptedFiltersSerializer(data=context.same_filter_above_json)


@then('validate the deserialized filters successfully')
def test(context):
    assert context.deserialized_data.is_valid() == True


@when('serialize the returned dorms data from the last filters')
def act(context):
    context.serialized_dorms = DormSerializer(context.filtered_dorms, many=True)
    context.serialized_dorms_string = str(context.serialized_dorms.data)


@then('get deserialize data for (only dovec with one room only)')
def test(context):
    print(context.serialized_dorms_string)
    assert context.serialized_dorms_string.count("('name', 'Dovec')") == 1


@when('hitting POST /dorms endpoint with filter above')
def act(context):
    request = APIRequestFactory().post(reverse('engine:dorms-list'),
                                       context.same_filter_above_json, format='json')
    view = DormViewSet.as_view(actions={'post': 'create'})
    context.response = view(request)


@then('get 200 OK with data for (only dovec with one room only)')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK

    returned_dorms = context.response.render().data[0]

    number_of_returned_json_filters = len(list(returned_dorms))
    assert number_of_returned_json_filters == 11

    print(context.response.render().data)
    assert str(context.response.render().data).count("('name', 'Dovec')") == 1
