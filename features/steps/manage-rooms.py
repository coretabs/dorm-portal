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
    # print(context.response.status_code)
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


@then('delete that third room in alfam')
def test(context):
    Dormitory.objects.get(name='Alfam').room_characteristics.all()[2].delete()


@when('hitting POST /manager/dorms/{alfam-id}/rooms')
def act(context):
    request = APIRequestFactory().post('', context.third_room_json, format='json')
    force_authenticate(request, context.john)
    view = RoomManagementViewSet.as_view(actions={'post': 'create'})
    context.response = view(request, dorm_pk=context.alfam.id)


@then('get 201 created for adding a third room in alfam')
def test(context):
    assert context.response.status_code == status.HTTP_201_CREATED
    assert Dormitory.objects.get(name='Alfam').room_characteristics.count() == 3


@when('hitting POST /manager/dorms/{alfam-id}/rooms for non-owned dorm')
def act(context):
    request = APIRequestFactory().post('', context.third_room_json, format='json')
    force_authenticate(request, context.scott)
    view = RoomManagementViewSet.as_view(actions={'post': 'create'})
    context.response = view(request, dorm_pk=context.alfam.id)


@then('get 403 forbidden for adding a third room in non-owned dorm')
def test(context):
    assert context.response.status_code == status.HTTP_403_FORBIDDEN


@given('total_quota=10, allowed_quota=5 for both rooms')
def arrange(context):
    context.room1.total_quota = 10
    context.room1.allowed_quota = 5
    context.room2.total_quota = 10
    context.room2.allowed_quota = 5

    context.room1.save()
    context.room2.save()


@given('first room in alfam has 2 reserved from its quota')
def arrange(context):
    context.user1 = create_student(context, 'Owen')
    context.user2 = create_student(context, 'Tia')
    context.reservation1 = create_reservation(context.room1, context.user1)
    context.reservation2 = create_reservation(context.room1, context.user2)


@given('second room in alfam has 1 reserved from its quota')
def arrange(context):
    context.user3 = create_student(context, 'Mako')
    context.reservation3 = create_reservation(context.room2, context.user3)


@when('asking for statistics for rooms in alfam')
def act(context):
    #context.reservations_statistics = Reservation.objects.status_statistics(context.alfam.id)
    context.room_with_stats = RoomCharacteristics.objects.with_reserved_rooms_number().all()


@then('room1 (total_quota=10, allowed_quota=3, reserved_rooms_number=2)')
def test(context):
    # print(context.room_with_stats[0].allowed_quota)
    assert context.room_with_stats[0].total_quota == 10
    assert context.room_with_stats[0].allowed_quota == 3
    assert context.room_with_stats[0].reserved_rooms_number == 2


@then('room2 (total_quota=10, allowed_quota=4, reserved_rooms_number=1)')
def test(context):
    # print(context.reservations_statistics['pending_reservations'])
    assert context.room_with_stats[1].total_quota == 10
    assert context.room_with_stats[1].allowed_quota == 4
    assert context.room_with_stats[1].reserved_rooms_number == 1


@when('serializing all rooms with statistics for alfam dorm')
def act(context):
    context.serialized_rooms = DormManagementRoomStatisticsSerializer(
        context.room_with_stats, many=True)
    context.rooms_string = str(context.serialized_rooms.data)


@then('get serialized rooms with statistics for alfam dorm')
def test(context):
    # print(context.rooms_string)
    assert context.rooms_string.count("'allowed_quota', 3") == 1


@when('hitting GET /manager/dorms/{alfam-id}/rooms')
def act(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.john)
    view = RoomManagementViewSet.as_view(actions={'get': 'list'})
    context.response = view(request, dorm_pk=context.alfam.id)


@then('get 200 OK with rooms statistics for alfam')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_200_OK
    # print(context.response.render().data)
    assert context.rooms_string.count("'allowed_quota', 3") == 1


@when('hitting GET /manager/dorms/{alfam-id}/rooms for non-owned dorm')
def act(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.scott)
    view = RoomManagementViewSet.as_view(actions={'get': 'list'})
    context.response = view(request, dorm_pk=context.alfam.id)


@then('get 403 forbidden for getting rooms statistics in non-owned dorm')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_403_FORBIDDEN
