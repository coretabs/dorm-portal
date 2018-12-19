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


"""
Given two managers (one for alfam&dovec and one for homedorm)
Given we have dorms(alfam & dovec & homedorm) + 2 rooms in alfam

Both these two scenarios implenetations exist in manage-dorm.py
"""


@given('two students reserved first room and one reserved second one')
def arrange(self):
    self.user1 = create_student(self, 'Owen')
    self.user2 = create_student(self, 'Tia')
    self.reservation1 = create_reservation(self.room1, self.user1)
    self.reservation2 = create_reservation(self.room2, self.user2)


@given('two user have expired reservations for room2')
def arrange(self):
    self.user3 = create_student(self, 'Mako')
    self.user4 = create_student(self, 'Lora')

    self.reservation3 = create_reservation(self.room2, self.user3)
    self.reservation4 = create_reservation(self.room2, self.user4)

    self.reservation3.confirmation_deadline_date = datetime.date.today()
    self.reservation3.save()
    self.reservation4.confirmation_deadline_date = datetime.date.today()
    self.reservation4.save()


@when('changing reservation status into rejected')
def act(self):
    self.quota_before_rejection = self.reservation1.room_characteristics.allowed_quota
    self.reservation1.update_status(Reservation.REJECTED_STATUS)
    self.reservation1 = Reservation.objects.get(pk=self.reservation1.id)


@then('quota of that room should increase by 1')
def test(self):
    assert self.reservation1.status == Reservation.REJECTED_STATUS
    assert self.reservation1.room_characteristics.allowed_quota == self.quota_before_rejection + 1


@when('asking for reservations status statistics by dorm_id')
def act(self):
    #self.reservations_statistics = models.Reservation.objects.status_statistics(self.alfam.id)
    self.reservations_statistics = models.Reservation.objects.status_statistics()


@then('get the correct reservations status statistics')
def test(self):
    # print(self.reservations_statistics['pending_reservations'])
    assert self.reservations_statistics['pending_reservations'] == 1
    assert self.reservations_statistics['rejected_reservations'] == 1
    assert self.reservations_statistics['confirmed_reservations'] == 0
    assert self.reservations_statistics['waiting_for_manager_action_reservations'] == 0
    assert self.reservations_statistics['manager_updated_reservations'] == 0
    assert self.reservations_statistics['expired_reservations'] == 2


@when('serializing all dorm reservations')
def act(self):
    self.reservations = Reservation.objects.filter(
        room_characteristics__dormitory__id=self.alfam.id)

    self.reservations_statistics['reservations'] = self.reservations.all()

    self.serialized_dorms = ReservationManagementSerializer(self.reservations_statistics)
    self.all_serialized_dorms = str(self.serialized_dorms.data)


@then('get valid serialized reservations')
def test(self):
    # print(self.all_serialized_dorms)
    assert self.all_serialized_dorms.count("'name', 'Mako'") == 1


@when('hitting GET /manager/dorms/{alfam-id}/reservations')
def act(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.john)
    view = ReservationManagementViewSet.as_view(actions={'get': 'list'})
    self.response = view(request, dorm_pk=self.alfam.id)


@then('get 200 OK with all the reservations')
def test(self):
    assert self.response.status_code == status.HTTP_200_OK

    # print(self.response.render().data)

    assert str(self.response.render().data).count("'name', 'Mako'") == 1


@when('hitting GET /manager/dorms/{homedorm-id}/reservations non-owned dorm')
def act(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.john)
    view = ReservationManagementViewSet.as_view(actions={'get': 'list'})
    self.response = view(request, dorm_pk=self.homedorm.id)


@then('get 403 forbidden for homedorm reservations')
def test(self):
    assert self.response.status_code == status.HTTP_403_FORBIDDEN


@then('the other manager can get his homedorm reservations')
def test(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.scott)
    view = ReservationManagementViewSet.as_view(actions={'get': 'list'})
    self.response = view(request, dorm_pk=self.homedorm.id)

    assert self.response.status_code == status.HTTP_200_OK


@when('deserializing reservation new data')
def act(self):
    self.reservation_new_data = {'confirmation_deadline_date': '2015-12-15',
                                 'status': Reservation.MANAGER_UPDATED_STATUS,
                                 'follow_up_message': 'Please upload your receipt again'}

    self.deserialized_data = ClientReservationManagementSerializer(data=self.reservation_new_data)


@then('get valid deserialized reservation data')
def test(self):
    assert self.deserialized_data.is_valid() == True


@when('hitting PUT /manager/dorms/{alfam-id}/reservations/{res1-id} into manager_updated')
def act(self):
    request = APIRequestFactory().put('', self.reservation_new_data, format='json')
    force_authenticate(request, self.john)
    view = ReservationManagementViewSet.as_view(actions={'put': 'update'})
    self.response = view(request, dorm_pk=self.alfam.id, pk=self.reservation1.id)


@then('get 200 OK for updating that reservation into manager_updated')
def test(self):
    assert self.response.status_code == status.HTTP_200_OK
    assert Reservation.objects.filter(id=self.reservation1.id).first(
    ).status == Reservation.MANAGER_UPDATED_STATUS


@when('hitting PUT non-owned reservation into manager_updated')
def act(self):
    request = APIRequestFactory().put('', self.reservation_new_data, format='json')
    force_authenticate(request, self.scott)
    view = ReservationManagementViewSet.as_view(actions={'put': 'update'})
    self.response = view(request, dorm_pk=self.alfam.id, pk=self.reservation1.id)


@then('get 403 forbidden for updating non-owned reservation')
def test(self):
    assert self.response.status_code == status.HTTP_403_FORBIDDEN
