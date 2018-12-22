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
def arrange(self):
    create_alfam_dovec_with_4_rooms(self)


@given('two students who reserved nothing')
def arrange(self):
    self.user1 = create_student(self, 'Owen')
    self.user2 = create_student(self, 'Tia')


@when('create a reservation')
def act(self):
    self.previous_quota = self.room1.allowed_quota
    self.reservation1 = create_reservation(self.room1, self.user1)


@then('quota of the room should decrease')
def test(self):
    assert self.room1.allowed_quota == self.previous_quota - 1


@then('deadline date should be equal to today+room_confirmation_days')
def test(self):
    """default room_confirmation_days is 2"""
    # print(datetime.date.today() + datetime.timedelta(days=2))
    # print(self.reservation1.confirmation_deadline_date)
    assert self.reservation1.confirmation_deadline_date == datetime.date.today() + datetime.timedelta(days=2)


@when('creating reservation for room 2 for same user')
def act(self):
    self.previous_quota = self.room1.allowed_quota

    self.reservation2 = create_reservation(self.room2, self.user1)

    self.room1 = RoomCharacteristics.objects.get(pk=self.room1.id)


@then('create a reservation for that student for room 2')
def test(self):
    assert self.user1.reservations.filter(id=self.reservation2.id).count() == 1


@then('first pending reservation should be deleted')
def test(self):
    assert Reservation.objects.filter(id=self.reservation1.id).count() == 0


@then('quota of that room increase')
def test(self):
    assert self.room1.allowed_quota == self.previous_quota + 1


@when('a reservation is non-pending and creating another reservation')
def act(self):
    self.reservation2.status = Reservation.WAITING_FOR_MANAGER_ACTION_STATUS
    self.reservation2.save()

    try:
        self.reservation3 = create_reservation(self.room1, self.user1)
        self.result_exception = None
    except Exception as e:
        self.result_exception = e

    self.user1 = User.objects.get(pk=self.user1.id)


@then('throw an exception for creating that reservation')
def test(self):
    assert self.result_exception != None
    assert isinstance(self.result_exception, NonFinishedUserReservationsException) == True


@then('if the reservation is confirmed, rejected, or expired')
def act(self):
    self.reservation2.status = Reservation.CONFIRMED_STATUS
    self.reservation2.save()
    self.reservation3 = create_reservation(self.room1, self.user1)
    self.user1 = User.objects.get(pk=self.user1.id)


@then('its okay to create another reservation')
def test(self):
    assert self.user1.reservations.filter(id=self.reservation2.id).count() == 1
    assert self.user1.reservations.filter(id=self.reservation3.id).count() == 1


@when('retrieving an expired reservation')
def act(self):
    self.reservation2.confirmation_deadline_date = datetime.date.today() - datetime.timedelta(days=1)
    self.reservation2.save()

    self.reservation2 = Reservation.objects.get(pk=self.reservation2.id).check_if_expired()


@then('change its status into expired and increase room quota')
def test(self):
    assert self.reservation2.status == Reservation.EXPIRED_STATUS


@given('cleanup all reservations')
def arrange(self):
    Reservation.objects.all().delete()
    assert Reservation.objects.count() == 0


@when('hitting POST /reservations for room 1')
def act(self):
    reservation_data = {'room_id': self.room1.id}

    request = APIRequestFactory().post('', reservation_data, format='json')
    force_authenticate(request, self.user1)
    view = ReservationViewSet.as_view(actions={'post': 'create'})
    self.response = view(request)


@then('get 201 Created for creating that reservation')
def test(self):
    # print(self.response.status_code)
    assert self.response.status_code == status.HTTP_201_CREATED
    assert Reservation.objects.count() == 1
    self.reservation1 = Reservation.objects.first()


@when('hitting POST /reservations with logging in')
def act(self):
    reservation_data = {'room_id': self.room1.id}

    request = APIRequestFactory().post('', reservation_data, format='json')
    view = ReservationViewSet.as_view(actions={'post': 'create'})
    self.response = view(request)


@then('get 403 Forbidden to ensure reservation after login')
def test(self):
    # print(self.response.status_code)
    assert self.response.status_code == status.HTTP_403_FORBIDDEN


@when('hitting POST /reservations and no quota left')
def act(self):
    self.room1.allowed_quota = 0
    self.room1.save()
    reservation_data = {'room_id': self.room1.id}

    request = APIRequestFactory().post('', reservation_data, format='json')
    force_authenticate(request, self.user1)
    view = ReservationViewSet.as_view(actions={'post': 'create'})
    self.response = view(request)


@then('get 400 Bad request to ensure using available quota')
def test(self):
    # print(self.response.status_code)
    assert self.response.status_code == status.HTTP_400_BAD_REQUEST


@when('hitting POST /reservations and he has a non-finished reservation')
def act(self):
    reservation_data = {'room_id': self.room1.id}

    request = APIRequestFactory().post('', reservation_data, format='json')
    force_authenticate(request, self.user1)
    view = ReservationViewSet.as_view(actions={'post': 'create'})
    self.response = view(request)


@then('get 400 Bad request to ensure finishing his reservation first')
def test(self):
    # print(self.response.status_code)
    assert self.response.status_code == status.HTTP_400_BAD_REQUEST


@when('serializing reservation data')
def act(self):
    self.serialized_reservation = ReservationDetailsSerializer(self.reservation1)
    self.all_serialized_reservation = str(self.serialized_reservation.data)


@then('get valid serialized data')
def test(self):
    # print(self.all_serialized_reservation)
    assert self.all_serialized_reservation.count("'confirmation_deadline_date'") == 1


@then('confirmation_deadline_date form is 2018-12-15')
def test(self):
    # print(self.serialized_reservation['confirmation_deadline_date'].value)
    expected_date = (datetime.date.today() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    assert self.serialized_reservation['confirmation_deadline_date'].value == expected_date


@when('hitting GET /reservations/{res-id}')
def act(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.user1)
    view = ReservationViewSet.as_view(actions={'get': 'retrieve'})
    self.response = view(request, pk=self.reservation1.id)


@then('get 200 OK and reservation details')
def test(self):
    assert self.response.status_code == status.HTTP_200_OK
    data_returned = str(self.response.render().data)
    # print(data_returned)
    assert data_returned.count("'confirmation_deadline_date'") == 1


@when('hitting GET /reservations/{res-id} for expired reservation')
def act(self):
    self.reservation1.confirmation_deadline_date = datetime.date.today() - datetime.timedelta(days=1)
    self.reservation1.save()

    request = APIRequestFactory().get('')
    force_authenticate(request, self.user1)
    view = ReservationViewSet.as_view(actions={'get': 'retrieve'})
    self.response = view(request, pk=self.reservation1.id)


@then('get 200 OK and the expired reservation')
def test(self):
    assert self.response.status_code == status.HTTP_200_OK
    data_returned = str(self.response.render().data)
    # print(data_returned)
    assert data_returned.count("'status': '5'") == 1


@when('hitting GET /reservations/{res-id} for non-owned reservation')
def act(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.user2)
    view = ReservationViewSet.as_view(actions={'get': 'retrieve'})
    self.response = view(request, pk=self.reservation1.id)


@then('get 403 Forbidden for non-owned reservation')
def test(self):
    assert self.response.status_code == status.HTTP_403_FORBIDDEN


@when('adding a receipt to a reservation')
def act(self):
    receipt = create_receipt_photo(self.reservation1)
    self.reservation1.add_receipt(receipt)
    self.reservation1.save()


@then('it should update the status into WAITING_FOR_MANAGER_ACTION_STATUS')
def test(self):
    assert self.reservation1.status == Reservation.WAITING_FOR_MANAGER_ACTION_STATUS
    assert self.reservation1.receipts.count() == 1


@then('adding a receipt to a rejected/confirmed/expired reservation')
def act(self):
    self.reservation1.status = Reservation.REJECTED_STATUS
    self.reservation1.save()

    try:
        receipt = create_receipt_photo(self.reservation1)
        self.reservation1.add_receipt(receipt)
        self.reservation1.save()
    except Exception as e:
        self.result_exception = e


@then('it should throw NonUpdatableReservationException')
def act(self):
    assert self.result_exception != None
    assert isinstance(self.result_exception, NonUpdatableReservationException) == True


@when('hitting POST /reservations/{res-id}/receipt to add new receipt')
def act(self):
    self.reservation1.status = Reservation.PENDING_STATUS
    self.reservation1.receipts.all().delete()
    self.reservation1.save()

    uploaded_file = create_uploaded_file(self, 'receipt.jpg')
    photo_json = {'uploaded_photo': uploaded_file}

    client = APIClient()
    client.force_authenticate(self.user1)

    url = reverse('engine.reservations:receipts-list',
                  kwargs={'reservation_pk': self.reservation1.id})
    self.response = client.post(url, photo_json, format='multipart')


@then('get 201 created for adding a receipt')
def test(self):
    # print(self.response.data)
    assert self.response.status_code == status.HTTP_201_CREATED
    assert Reservation.objects.first().receipts.count() == 1

    assert os.path.exists(self.expected_file_path) == True
    os.remove(self.expected_file_path)


@when('hitting POST /reservations/{res-id}/receipt for rejected/confirmed/expired')
def act(self):
    self.reservation1.status = Reservation.REJECTED_STATUS
    self.reservation1.receipts.all().delete()
    self.reservation1.save()

    uploaded_file = create_uploaded_file(self, 'receipt.jpg')
    photo_json = {'uploaded_photo': uploaded_file}

    client = APIClient()
    client.force_authenticate(self.user1)

    url = reverse('engine.reservations:receipts-list',
                  kwargs={'reservation_pk': self.reservation1.id})
    self.response = client.post(url, photo_json, format='multipart')


@then('get 400 bad request for not updatable reservation')
def test(self):
    # print(self.response.data)
    assert self.response.status_code == status.HTTP_400_BAD_REQUEST


@when('hitting POST /reservations/{res-id}/receipt non-owned reservation')
def act(self):
    self.reservation1.status = Reservation.PENDING_STATUS
    self.reservation1.receipts.all().delete()
    self.reservation1.save()

    uploaded_file = create_uploaded_file(self, 'receipt.jpg')
    photo_json = {'uploaded_photo': uploaded_file}

    client = APIClient()
    client.force_authenticate(self.user2)

    url = reverse('engine.reservations:receipts-list',
                  kwargs={'reservation_pk': self.reservation1.id})
    self.response = client.post(url, photo_json, format='multipart')


@then('get forbidden 403 for non-owned reservation')
def test(self):
    # print(self.response.data)
    assert self.response.status_code == status.HTTP_403_FORBIDDEN
