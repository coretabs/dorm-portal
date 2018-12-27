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


@given('we have radio filters (meals, balcony-size)')
def arrange(context):
    context.meal_options = [RadioOption(name='Breakfast'), RadioOption(name='Dinner')]
    context.meals = create_radio_filter(
        context.meal_options, LazyI18nString({'tr': 'Yemekler', 'en': 'Meals'}))
    context.meals_choice_breakfast = create_radio_choice(context.meal_options[0], context.meals)
    context.meals_choice_dinner = create_radio_choice(context.meal_options[1], context.meals)

    context.balcony_size_options = [RadioOption(
        name='Big Balcony'), RadioOption(name='Small Balcony')]
    context.balcony_size = create_radio_filter(
        context.balcony_size_options, LazyI18nString({'tr': 'Balkon', 'en': 'Baclony Size'}))
    context.balcony_size_choice_big = create_radio_choice(
        context.balcony_size_options[0], context.balcony_size)
    context.balcony_size_choice_small = create_radio_choice(
        context.balcony_size_options[1], context.balcony_size)


@given('we have integral filters (bathrooms, cookers)')
def arrange(context):
    context.bathrooms = IntegralFilter(name=LazyI18nString({'tr': 'Banyo', 'en': 'Bathroom'}))
    context.bathrooms.save()
    context.bathrooms1 = create_integral_choice(context.bathrooms, 1)
    context.bathrooms2 = create_integral_choice(context.bathrooms, 2)

    context.cookers = IntegralFilter(name=LazyI18nString({'tr': 'Ocak', 'en': 'Cooker'}))
    context.cookers.save()
    context.cookers1 = create_integral_choice(context.cookers, 1)
    context.cookers2 = create_integral_choice(context.cookers, 2)


@given('we have feature filters (shower, air-conditioner)')
def arrange(context):
    context.luxury_shower = create_room_feature(
        LazyI18nString({'tr': 'Lüks Duş', 'en': 'Luxury shower'}))
    context.air_conditioner = create_room_feature(
        LazyI18nString({'tr': 'Klima', 'en': 'Air Conditioner'}))


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

    context.deserialized_data = DormManagementNewRoomSerializer(data=context.third_room_json,
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
    assert str(context.response.render().data).count("'allowed_quota', 3") == 1


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


@given('second room in alfam has (big-balcony, 2-bathrooms, shower)')
def arrange(context):
    context.room2.radio_choices.add(context.balcony_size_choice_big)

    context.room2.integral_choices.add(context.bathrooms2)

    context.room2.features.add(context.luxury_shower)

    context.room2.save()


@when('asking for second room with its filters and choices')
def act(context):
    context.second_room_with_filters = RoomCharacteristics.objects.with_all_filters_and_choices(
        context.room2.id)


@then('get second room with its filters and choices')
def test(context):
    # print(context.second_room_with_filters)
    # -1 is the default result

    assert context.second_room_with_filters.radio_filters.count() == 2
    assert context.second_room_with_filters.radio_filters.get(
        name__contains='Meals').chosen_option_id == -1
    assert context.second_room_with_filters.radio_filters.get(
        name__contains='Baclony Size').chosen_option_id == context.balcony_size_choice_big.id

    assert context.second_room_with_filters.integral_filters.count() == 2
    assert context.second_room_with_filters.integral_filters.get(
        name__contains='Bathroom').selected_number == 2
    assert context.second_room_with_filters.integral_filters.get(
        name__contains='Cooker').selected_number == -1

    assert context.second_room_with_filters.all_features.count() == 2


@when('serialize second room with its filters and choices')
def act(context):
    context.serialized_room = DormManagementRoomDetailsSerializer(context.second_room_with_filters)
    context.room_string = str(context.serialized_room.data)


@then('get serialized second room with its filters and choices')
def test(context):
    # print(context.room_string)
    assert context.room_string.count("'chosen_option_id', -1") == 1


@when('hitting GET /manager/dorms/{alfam-id}/rooms/{room2-id}')
def act(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.john)
    view = RoomManagementViewSet.as_view(actions={'get': 'retrieve'})
    context.response = view(request, dorm_pk=context.alfam.id, pk=context.room2.id)


@then('get 200 OK with second room (filters and choices as well)')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_200_OK
    # print(context.response.render().data)
    assert str(context.response.render().data).count("'chosen_option_id', -1") == 1


@when('deserializing data to update second room in alfam')
def act(context):
    context.second_room_new_data = {
        'total_quota': 20,
        'allowed_quota': 9,
        'room_type_id': context.room_type_double_choice.id,
        'people_allowed_number': 3,
        'price': 3000,
        'currency_id': context.usd.id,
        'room_confirmation_days': 6,
        'duration_id': context.duration_choice_spring.id,
        'room_features': [context.luxury_shower.id, context.air_conditioner.id],
        'radio_choices': [context.meals_choice_dinner.id, context.balcony_size_choice_small.id],
        'integral_choices': [{'id': context.bathrooms.id, 'selected_number': 5},
                             {'id': context.cookers.id, 'selected_number': 2}]
    }

    context.deserialized_data = DormManagementEditRoomSerializer(context.room2,
                                                                 data=context.second_room_new_data,
                                                                 partial=True)


@then('validate the deserialized data to update room in alfam')
def test(context):
    # context.deserialized_data.is_valid()
    # print(context.deserialized_data.errors)
    assert context.deserialized_data.is_valid() == True


@then('update the second room in alfam successfully')
def test(context):
    context.deserialized_data.save()
    # print(context.deserialized_data)

    second_room_after_update = RoomCharacteristics.objects.get(pk=context.room2.id)

    assert second_room_after_update.total_quota == 20
    assert second_room_after_update.allowed_quota == 9
    assert second_room_after_update.room_confirmation_days == 6

    assert second_room_after_update.features.count() == 2
    assert second_room_after_update.features.get(pk=context.luxury_shower.id) != None
    assert second_room_after_update.features.get(pk=context.air_conditioner.id) != None

    assert second_room_after_update.radio_choices.count() == 4
    assert second_room_after_update.radio_choices.get(
        pk=context.room_type_double_choice.id) != None
    assert second_room_after_update.radio_choices.get(
        pk=context.duration_choice_spring.id) != None
    assert second_room_after_update.radio_choices.get(
        pk=context.meals_choice_dinner.id) != None
    assert second_room_after_update.radio_choices.get(
        pk=context.balcony_size_choice_small.id) != None

    assert second_room_after_update.integral_choices.count() == 4
    assert second_room_after_update.integral_choices.get(
        related_filter__name__contains='Price').selected_number == 3000
    assert second_room_after_update.integral_choices.get(
        related_filter__name__contains='People Allowed Number').selected_number == 3
    assert second_room_after_update.integral_choices.get(
        related_filter__name__contains='Bathroom').selected_number == 5
    assert second_room_after_update.integral_choices.get(
        related_filter__name__contains='Cooker').selected_number == 2


@when('hitting PUT /manager/dorms/{alfam-id}/rooms/{room2-id}')
def act(context):
    request = APIRequestFactory().put('', context.second_room_new_data, format='json')
    force_authenticate(request, context.john)
    view = RoomManagementViewSet.as_view(actions={'put': 'update'})
    context.response = view(request, dorm_pk=context.alfam.id, pk=context.room2.id)


@then('get 200 OK with for updating that room')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK


@when('hitting POST /manager/dorms/{alfma-id}/rooms/{room2-id}/photos')
def act(context):
    uploaded_file = create_uploaded_file(context, 'room-photo.jpeg')
    photo_json = {'uploaded_photo': uploaded_file}

    client = APIClient()
    client.force_authenticate(context.john)

    url = reverse('engine.manager-dorms.rooms:photos-list', kwargs={'dorm_pk': context.alfam.id,
                                                                    'room_pk': context.room2.id})
    context.response = client.post(url, photo_json, format='multipart')


@then('get 201 created for adding a photo in room2')
def test(context):
    assert context.response.status_code == status.HTTP_201_CREATED

    assert RoomCharacteristics.objects.get(pk=context.room2.id).photos.count() == 1

    assert os.path.exists(context.expected_file_path) == True
    # os.remove(context.expected_file_path)


@when('hitting POST /manager/dorms/{alfma-id}/rooms/{room2-id}/photos for non-owned dorm')
def act(context):
    uploaded_file = create_uploaded_file(context, 'room-photo.jpeg')
    photo_json = {'uploaded_photo': uploaded_file}

    client = APIClient()
    client.force_authenticate(context.scott)

    url = reverse('engine.manager-dorms.rooms:photos-list', kwargs={'dorm_pk': context.alfam.id,
                                                                    'room_pk': context.room2.id})
    context.response = client.post(url, photo_json, format='multipart')


@then('get 403 forbidden for adding a photo in room2 in non-owned dorm')
def test(context):
    assert context.response.status_code == status.HTTP_403_FORBIDDEN


@when('hitting DELETE /manager/dorms/{alfam-id}/rooms/{room2-id}/photos/{alfam-photo-id}')
def act(context):
    room_photo = RoomCharacteristics.objects.get(pk=context.room2.id).photos.first()

    request = APIRequestFactory().delete('')
    force_authenticate(request, context.john)
    view = PhotoRoomManagementViewSet.as_view(actions={'delete': 'destroy'})
    context.response = view(request, dorm_pk=context.alfam.id,
                            room_pk=context.room2.pk,
                            pk=room_photo.id)


@then('get 204 noContent for deleting the photo from the second room')
def test(context):
    assert context.response.status_code == status.HTTP_204_NO_CONTENT
    assert RoomCharacteristics.objects.get(pk=context.room2.id).photos.count() == 0
    assert os.path.exists(context.expected_file_path) == False
