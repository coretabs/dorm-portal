import os

from django.urls import reverse

from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from rest_framework import status

from behave import given, when, then

from i18nfield.strings import LazyI18nString

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


@when('getting manager filters to add to a room from serializer')
def act(context):
    context.serialized_room_filters = DormManagementRoomFiltersSerializer([])
    context.room_filters_string = str(context.serialized_room_filters.data)


@then('get valid serialized room filters')
def test(context):
    # print(context.room_filters_string)
    assert context.room_filters_string.count("'name', 'Single'") == 1


@when('hitting GET /manager-dorms/filters')
def act(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.john)
    view = DormManagementViewSet.as_view(actions={'get': 'filters'})
    context.response = view(request)


@then('get 200 OK with filters')
def test(context):
    print(context.response.status_code)
    assert context.response.status_code == status.HTTP_200_OK
    # print(context.response.render().data)
    assert str(context.response.render().data).count("'name', 'Single'") == 1


@when('deserializing the third room data')
def act(context):
    context.third_room_json = {
        'total_quota': 5,
        'allowed_quota': 2,
        'room_type_id': context.room_type_single_choice.id,
        'people_allowed_number': 2,
        'price': 2000,
        'currency_id': context.usd.id,
        'room_confirmation_days': 5,
        'duration_id': context.duration_choice_spring.id,
        'room_features': [context.luxury_shower.id],
        'radio_choices': [context.meals_choice_breakfast.id],
        'integral_choices': [{'id': context.bathrooms.id, 'selected_number': 3}]
    }

    context.deserialized_data = DormManagemenNewRoomSerializer(data=context.third_room_json,
                                                               context={'dorm_pk': context.alfam.id})


@then('validate the deserialized data of the third room')
def test(context):
    # context.deserialized_data.is_valid()
    # print(context.deserialized_data.errors)
    assert context.deserialized_data.is_valid() == True


@then('save the third room to alfam')
def test(context):
    context.deserialized_data.save()
    assert Dormitory.objects.get(name='Alfam').room_characteristics.count() == 3
    # print(context.deserialized_data)

    new_room = Dormitory.objects.get(name='Alfam').room_characteristics.all()[2]
    assert new_room.features.count() == 1
    assert new_room.radio_choices.count() == 3
    assert new_room.integral_choices.count() == 3
