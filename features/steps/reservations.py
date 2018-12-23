import os
import datetime

from django.urls import reverse

from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from rest_framework import status

from behave import given, when, then

from i18nfield.strings import LazyI18nString

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *
from api.engine.exceptions import *

from features.steps.factory import *


@given('we have 2 dormitories (and 1 room each available to reserve)')
def arrange(context):
    create_alfam_dovec_with_4_rooms(context)


@given('two students who reserved nothing')
def arrange(context):
    context.user1 = create_student(context, 'Owen')
    context.user2 = create_student(context, 'Tia')


@when('create a reservation')
def act(context):
    context.previous_quota = context.room1.allowed_quota
    context.reservation1 = create_reservation(context.room1, context.user1)


@then('quota of the room should decrease')
def test(context):
    context.room1 = RoomCharacteristics.objects.get(pk=context.room1.id)
    assert context.room1.allowed_quota == context.previous_quota - 1


@then('deadline date should be equal to today+room_confirmation_days')
def test(context):
    """default room_confirmation_days is 2"""
    # print(datetime.date.today() + datetime.timedelta(days=2))
    # print(context.reservation1.confirmation_deadline_date)
    assert context.reservation1.confirmation_deadline_date == datetime.date.today() + \
        datetime.timedelta(days=2)


@when('create a reservation for the same room')
def act(context):
    context.previous_quota = context.room1.allowed_quota
    context.reservation1 = create_reservation(context.room1, context.user1)


@then('quota of the room should be the same')
def test(context):
    context.room1 = RoomCharacteristics.objects.get(pk=context.room1.id)
    assert context.room1.allowed_quota == context.previous_quota


@when('creating reservation for room 2 for same user')
def act(context):
    context.previous_quota = context.room1.allowed_quota

    context.reservation2 = create_reservation(context.room2, context.user1)

    context.room1 = RoomCharacteristics.objects.get(pk=context.room1.id)


@then('create a reservation for that student for room 2')
def test(context):
    assert context.user1.reservations.filter(id=context.reservation2.id).count() == 1


@then('first pending reservation should be deleted')
def test(context):
    assert Reservation.objects.filter(id=context.reservation1.id).count() == 0


@then('quota of that room increase')
def test(context):
    assert context.room1.allowed_quota == context.previous_quota + 1


@when('a reservation is non-pending and creating another reservation')
def act(context):
    context.reservation2.status = Reservation.WAITING_FOR_MANAGER_ACTION_STATUS
    context.reservation2.save()

    try:
        context.reservation3 = create_reservation(context.room1, context.user1)
        context.result_exception = None
    except Exception as e:
        context.result_exception = e

    context.user1 = User.objects.get(pk=context.user1.id)


@then('throw an exception for creating that reservation')
def test(context):
    assert context.result_exception != None
    assert isinstance(context.result_exception, NonFinishedUserReservationsException) == True


@then('if the reservation is confirmed, rejected, or expired')
def act(context):
    context.reservation2.status = Reservation.CONFIRMED_STATUS
    context.reservation2.save()
    context.reservation3 = create_reservation(context.room1, context.user1)
    context.user1 = User.objects.get(pk=context.user1.id)


@then('its okay to create another reservation')
def test(context):
    assert context.user1.reservations.filter(id=context.reservation2.id).count() == 1
    assert context.user1.reservations.filter(id=context.reservation3.id).count() == 1


@when('retrieving an expired reservation')
def act(context):
    context.reservation2.confirmation_deadline_date = datetime.date.today() - datetime.timedelta(days=1)
    context.reservation2.save()

    context.reservation2 = Reservation.objects.get(pk=context.reservation2.id).check_if_expired()


@then('change its status into expired and increase room quota')
def test(context):
    assert context.reservation2.status == Reservation.EXPIRED_STATUS


@given('cleanup all reservations')
def arrange(context):
    Reservation.objects.all().delete()
    assert Reservation.objects.count() == 0


@when('hitting POST /reservations for room 1')
def act(context):
    reservation_data = {'room_id': context.room1.id}

    request = APIRequestFactory().post('', reservation_data, format='json')
    force_authenticate(request, context.user1)
    view = ReservationViewSet.as_view(actions={'post': 'create'})
    context.response = view(request)


@then('get 201 Created for creating that reservation')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_201_CREATED
    assert Reservation.objects.count() == 1
    context.reservation1 = Reservation.objects.first()


@then('cleanup the created reservation')
def act(context):
    context.reservation1.delete()


@when('hitting POST /reservations with logging in')
def act(context):
    reservation_data = {'room_id': context.room1.id}

    request = APIRequestFactory().post('', reservation_data, format='json')
    view = ReservationViewSet.as_view(actions={'post': 'create'})
    context.response = view(request)


@then('get 403 Forbidden to ensure reservation after login')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_403_FORBIDDEN


@when('hitting POST /reservations and no quota left')
def act(context):
    context.room1.allowed_quota = 0
    context.room1.save()
    reservation_data = {'room_id': context.room1.id}

    request = APIRequestFactory().post('', reservation_data, format='json')
    force_authenticate(request, context.user1)
    view = ReservationViewSet.as_view(actions={'post': 'create'})
    context.response = view(request)


@then('get 400 Bad request to ensure using available quota')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST


@when('hitting POST /reservations and he has a non-finished reservation')
def act(context):
    reservation_data = {'room_id': context.room1.id}

    request = APIRequestFactory().post('', reservation_data, format='json')
    force_authenticate(request, context.user1)
    view = ReservationViewSet.as_view(actions={'post': 'create'})
    context.response = view(request)


@then('get 400 Bad request to ensure finishing his reservation first')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST


@when('serializing reservation data')
def act(context):
    context.serialized_reservation = ReservationDetailsSerializer(context.reservation1)
    context.all_serialized_reservation = str(context.serialized_reservation.data)


@then('get valid serialized data')
def test(context):
    # print(context.all_serialized_reservation)
    assert context.all_serialized_reservation.count("'confirmation_deadline_date'") == 1


@then('confirmation_deadline_date form is 2018-12-15')
def test(context):
    # print(context.serialized_reservation['confirmation_deadline_date'].value)
    expected_date = (datetime.date.today() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    assert context.serialized_reservation['confirmation_deadline_date'].value == expected_date


@when('hitting GET /reservations/{res-id}')
def act(context):
    context.room1.allowed_quota = 5
    context.room1.save()
    context.reservation1 = create_reservation(context.room1, context.user1)

    request = APIRequestFactory().get('')
    force_authenticate(request, context.user1)
    view = ReservationViewSet.as_view(actions={'get': 'retrieve'})
    context.response = view(request, pk=context.reservation1.id)


@then('get 200 OK and reservation details')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    data_returned = str(context.response.render().data)
    # print(data_returned)
    assert data_returned.count("'confirmation_deadline_date'") == 1


@when('hitting GET /reservations/{res-id} for expired reservation')
def act(context):
    context.reservation1.confirmation_deadline_date = datetime.date.today() - datetime.timedelta(days=1)
    context.reservation1.save()

    request = APIRequestFactory().get('')
    force_authenticate(request, context.user1)
    view = ReservationViewSet.as_view(actions={'get': 'retrieve'})
    context.response = view(request, pk=context.reservation1.id)


@then('get 200 OK and the expired reservation')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    data_returned = str(context.response.render().data)
    # print(data_returned)
    assert data_returned.count("'status': '5'") == 1


@when('hitting GET /reservations/{res-id} for non-owned reservation')
def act(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.user2)
    view = ReservationViewSet.as_view(actions={'get': 'retrieve'})
    context.response = view(request, pk=context.reservation1.id)


@then('get 403 Forbidden for non-owned reservation')
def test(context):
    assert context.response.status_code == status.HTTP_403_FORBIDDEN


@when('adding a receipt to a reservation')
def act(context):
    receipt = create_receipt_photo(context.reservation1)
    context.reservation1.add_receipt(receipt)
    context.reservation1.save()


@then('it should update the status into WAITING_FOR_MANAGER_ACTION_STATUS')
def test(context):
    assert context.reservation1.status == Reservation.WAITING_FOR_MANAGER_ACTION_STATUS
    assert context.reservation1.receipts.count() == 1


@then('adding a receipt to a rejected/confirmed/expired reservation')
def act(context):
    context.reservation1.status = Reservation.REJECTED_STATUS
    context.reservation1.save()

    try:
        receipt = create_receipt_photo(context.reservation1)
        context.reservation1.add_receipt(receipt)
        context.reservation1.save()
    except Exception as e:
        context.result_exception = e


@then('it should throw NonUpdatableReservationException')
def act(context):
    assert context.result_exception != None
    assert isinstance(context.result_exception, NonUpdatableReservationException) == True


@when('hitting POST /reservations/{res-id}/receipts to add new receipt')
def act(context):
    context.reservation1.status = Reservation.PENDING_STATUS
    context.reservation1.receipts.all().delete()
    context.reservation1.save()

    uploaded_file = create_uploaded_file(context, 'receipt.jpg')
    photo_json = {'uploaded_photo': uploaded_file}

    client = APIClient()
    client.force_authenticate(context.user1)

    url = reverse('engine.reservations:receipts-list',
                  kwargs={'reservation_pk': context.reservation1.id})
    context.response = client.post(url, photo_json, format='multipart')


@then('get 201 created for adding a receipt')
def test(context):
    # print(context.response.data)
    assert context.response.status_code == status.HTTP_201_CREATED
    assert Reservation.objects.first().receipts.count() == 1

    assert os.path.exists(context.expected_file_path) == True
    os.remove(context.expected_file_path)


@when('hitting POST /reservations/{res-id}/receipts for rejected/confirmed/expired')
def act(context):
    context.reservation1.status = Reservation.REJECTED_STATUS
    context.reservation1.receipts.all().delete()
    context.reservation1.save()

    uploaded_file = create_uploaded_file(context, 'receipt.jpg')
    photo_json = {'uploaded_photo': uploaded_file}

    client = APIClient()
    client.force_authenticate(context.user1)

    url = reverse('engine.reservations:receipts-list',
                  kwargs={'reservation_pk': context.reservation1.id})
    context.response = client.post(url, photo_json, format='multipart')


@then('get 400 bad request for not updatable reservation')
def test(context):
    # print(context.response.data)
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST


@when('hitting POST /reservations/{res-id}/receipts non-owned reservation')
def act(context):
    context.reservation1.status = Reservation.PENDING_STATUS
    context.reservation1.receipts.all().delete()
    context.reservation1.save()

    uploaded_file = create_uploaded_file(context, 'receipt.jpg')
    photo_json = {'uploaded_photo': uploaded_file}

    client = APIClient()
    client.force_authenticate(context.user2)

    url = reverse('engine.reservations:receipts-list',
                  kwargs={'reservation_pk': context.reservation1.id})
    context.response = client.post(url, photo_json, format='multipart')


@then('get forbidden 403 for non-owned reservation')
def test(context):
    # print(context.response.data)
    assert context.response.status_code == status.HTTP_403_FORBIDDEN
