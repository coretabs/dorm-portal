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
def arrange(context):
    context.user1 = create_student(context, 'Owen')
    context.user2 = create_student(context, 'Tia')
    context.reservation1 = create_reservation(context.room1, context.user1)
    context.reservation2 = create_reservation(context.room2, context.user2)

    context.reservation1.confirmation_deadline_date = datetime.date.today()
    context.reservation1.save()

    context.reservation2.confirmation_deadline_date = datetime.date.today() - datetime.timedelta(days=1)
    context.reservation2.save()


@given('two user have expired reservations for room2')
def arrange(context):
    context.user3 = create_student(context, 'Mako')
    context.user4 = create_student(context, 'Lora')

    context.reservation3 = create_reservation(context.room2, context.user3)
    context.reservation4 = create_reservation(context.room2, context.user4)

    context.reservation3.confirmation_deadline_date = datetime.date.today() - datetime.timedelta(days=2)
    context.reservation3.save()
    context.reservation4.confirmation_deadline_date = datetime.date.today() - datetime.timedelta(days=2)
    context.reservation4.save()


@when('updating expired reservations')
def act(context):
    context.reservations_statistics = models.Reservation.objects.update_expired_reservations()


@then('res3 & res4 will get expired')
def test(context):
    context.reservation3 = models.Reservation.objects.get(pk=context.reservation3.id)
    context.reservation4 = models.Reservation.objects.get(pk=context.reservation4.id)
    assert context.reservation3.status == Reservation.EXPIRED_STATUS
    assert context.reservation4.status == Reservation.EXPIRED_STATUS


@then('res1 & res2 are not expired')
def test(context):
    context.reservation1 = models.Reservation.objects.get(pk=context.reservation1.id)
    context.reservation2 = models.Reservation.objects.get(pk=context.reservation2.id)
    assert context.reservation1.status == Reservation.PENDING_STATUS
    assert context.reservation2.status == Reservation.PENDING_STATUS


@when('changing reservation status into rejected')
def act(context):
    context.quota_before_rejection = context.reservation1.room_characteristics.allowed_quota
    context.reservation1.update_status(Reservation.REJECTED_STATUS)
    context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)


@then('quota of that room should increase by 1')
def test(context):
    assert context.reservation1.status == Reservation.REJECTED_STATUS
    assert context.reservation1.room_characteristics.allowed_quota == context.quota_before_rejection + 1


@when('asking for reservations status statistics by dorm_id')
def act(context):
    #context.reservations_statistics = models.Reservation.objects.status_statistics(context.alfam.id)
    context.reservations_statistics = models.Reservation.objects.status_statistics()


@then('get the correct reservations status statistics')
def test(context):
    # print(context.reservations_statistics['pending_reservations'])
    assert context.reservations_statistics['pending_reservations'] == 1
    assert context.reservations_statistics['rejected_reservations'] == 1
    assert context.reservations_statistics['confirmed_reservations'] == 0
    assert context.reservations_statistics['waiting_for_manager_action_reservations'] == 0
    assert context.reservations_statistics['manager_updated_reservations'] == 0
    assert context.reservations_statistics['expired_reservations'] == 2


@when('serializing all dorm reservations')
def act(context):
    context.reservations = Reservation.objects.filter(
        room_characteristics__dormitory__id=context.alfam.id)

    context.reservations_statistics['reservations'] = context.reservations.all()

    context.serialized_dorms = ReservationManagementSerializer(context.reservations_statistics)
    context.all_serialized_dorms = str(context.serialized_dorms.data)


@then('get valid serialized reservations')
def test(context):
    # print(context.all_serialized_dorms)
    assert context.all_serialized_dorms.count("'student_name', 'Mako'") == 1


@when('hitting GET /manager-dorms/{alfam-id}/reservations')
def act(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.john)
    view = ReservationManagementViewSet.as_view(actions={'get': 'list'})
    context.response = view(request, dorm_pk=context.alfam.id)


@then('get 200 OK with all the reservations')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK

    # print(context.response.render().data)

    assert str(context.response.render().data).count("'student_name', 'Mako'") == 1


@when('hitting GET /manager-dorms/{homedorm-id}/reservations non-owned dorm')
def act(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.john)
    view = ReservationManagementViewSet.as_view(actions={'get': 'list'})
    context.response = view(request, dorm_pk=context.homedorm.id)


@then('get 403 forbidden for homedorm reservations')
def test(context):
    assert context.response.status_code == status.HTTP_403_FORBIDDEN


@then('the other manager can get his homedorm reservations')
def test(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.scott)
    view = ReservationManagementViewSet.as_view(actions={'get': 'list'})
    context.response = view(request, dorm_pk=context.homedorm.id)

    assert context.response.status_code == status.HTTP_200_OK


@when('deserializing reservation new data')
def act(context):
    context.reservation_new_data = {'confirmation_deadline_date': '2015-12-15',
                                    'status': Reservation.MANAGER_UPDATED_STATUS,
                                    'follow_up_message': 'Please upload your receipt again'}

    context.deserialized_data = ClientReservationManagementSerializer(
        data=context.reservation_new_data)


@then('get valid deserialized reservation data')
def test(context):
    assert context.deserialized_data.is_valid() == True


@when('hitting PUT /manager-dorms/{alfam-id}/reservations/{res1-id} into manager_updated')
def act(context):
    request = APIRequestFactory().put('', context.reservation_new_data, format='json')
    force_authenticate(request, context.john)
    view = ReservationManagementViewSet.as_view(actions={'put': 'update'})
    context.response = view(request, dorm_pk=context.alfam.id, pk=context.reservation1.id)


@then('get 200 OK for updating that reservation into manager_updated')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    assert Reservation.objects.filter(id=context.reservation1.id).first(
    ).status == Reservation.MANAGER_UPDATED_STATUS


@when('hitting PUT non-owned reservation into manager_updated')
def act(context):
    request = APIRequestFactory().put('', context.reservation_new_data, format='json')
    force_authenticate(request, context.scott)
    view = ReservationManagementViewSet.as_view(actions={'put': 'update'})
    context.response = view(request, dorm_pk=context.alfam.id, pk=context.reservation1.id)


@then('get 403 forbidden for updating non-owned reservation')
def test(context):
    assert context.response.status_code == status.HTTP_403_FORBIDDEN
