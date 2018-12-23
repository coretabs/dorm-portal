import os

from django.urls import reverse
from django.contrib.sites.models import Site
from django.core import mail
from django.conf import settings

from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from rest_framework import status

from freezegun import freeze_time

from behave import given, when, then

from i18nfield.strings import LazyI18nString

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


settings.IS_ALWAYS_REVIEWABLE = False


@when('both reservations arent confirmed')
def act(context):
    context.reservation1.status = Reservation.PENDING_STATUS
    context.reservation2.status = Reservation.PENDING_STATUS
    context.reservation1.save()
    context.reservation2.save()


@then('is_reviewable is false for non-confirmed reservations')
def test(context):
    context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)
    context.reservation2 = Reservation.objects.get(pk=context.reservation2.id)
    assert context.reservation1.is_reviewable == False
    assert context.reservation2.is_reviewable == False


@when('reservation is confirmed and after three months')
def act(context):
    context.reservation1.status = Reservation.CONFIRMED_STATUS
    context.reservation2.status = Reservation.CONFIRMED_STATUS

    context.reservation1.save()
    context.reservation2.save()


@then('is_reviewable is true for confirmed past 3 months reservation')
def test(context):
    context.reservation_creation_date_plus_three_months = context.reservation2.reservation_creation_date + \
        datetime.timedelta(days=90)

    with freeze_time(context.reservation_creation_date_plus_three_months):
        context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)
        context.reservation2 = Reservation.objects.get(pk=context.reservation2.id)
        # print(datetime.date.today())
        assert context.reservation1.is_reviewable == True
        assert context.reservation2.is_reviewable == True


@when('reservation is confirmed and before three months')
def act(context):
    context.reservation1.status = Reservation.CONFIRMED_STATUS
    context.reservation2.status = Reservation.CONFIRMED_STATUS

    context.reservation1.save()
    context.reservation2.save()


@then('is_reviewable is false for confirmed less 3 months reservation')
def test(context):
    context.reservation_creation_date_plus_two_months = context.reservation2.reservation_creation_date + \
        datetime.timedelta(days=60)

    with freeze_time(context.reservation_creation_date_plus_two_months):
        context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)
        context.reservation2 = Reservation.objects.get(pk=context.reservation2.id)
        # print(datetime.date.today())
        assert context.reservation1.is_reviewable == False
        assert context.reservation2.is_reviewable == False


@when('reservation is already reviewed')
def act(context):
    context.reservation1.is_reviewed = True
    context.reservation2.is_reviewed = False

    context.reservation1.save()
    context.reservation2.save()


@then('is_reviewable is false for already reviewed reservation')
def test(context):
    context.reservation_creation_date_plus_two_months = context.reservation2.reservation_creation_date + \
        datetime.timedelta(days=90)

    with freeze_time(context.reservation_creation_date_plus_two_months):
        context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)
        context.reservation2 = Reservation.objects.get(pk=context.reservation2.id)
        # print(datetime.date.today())
        assert context.reservation1.is_reviewable == False
        assert context.reservation2.is_reviewable == True


@then('return the first reservation is_reviewed into false')
def test(context):
    context.reservation1.is_reviewed = False
    context.reservation1.save()
    context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)


@when('asking for review and saving')
def act(context):
    context.site = Site(domain='http://127.0.0.1:8000', name='127.0.0.1')
    context.site.save()
    settings.SITE_ID = context.site.id

    context.asking_reservation = {'reservation_id': context.reservation1.id}
    context.deserialized_data = AskForReviewSerializer(
        data=context.asking_reservation)


@then('validate data and send email for review asking')
def test(context):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

    with freeze_time(context.reservation_creation_date_plus_two_months):
        assert context.deserialized_data.is_valid() == True
        assert len(mail.outbox) == 0

        context.deserialized_data.save()
        #assert len(mail.outbox) == 1


@when('hitting POST /manager/dorms/{alfam-id}/reservations/{res-id}/ask-review')
def act(context):
    #request = APIRequestFactory().post('')
    #force_authenticate(request, context.john)
    #view = ReservationManagementViewSet.as_view(actions={'post': 'ask_review'})
    #context.response = view(request, dorm_pk=context.alfam.id, pk=context.reservation1.id)
    with freeze_time(context.reservation_creation_date_plus_two_months):
        client = APIClient()
        client.force_authenticate(context.john)
        url = reverse('engine.dorms:reservations-ask-review',
                      kwargs={'dorm_pk': context.alfam.id, 'pk': context.reservation1.id})
        context.response = client.post(url)
        print(len(mail.outbox))


@then('get 200 OK for sending review email')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_200_OK


@when('hitting POST /manager/dorms/{alfam-id}/reservations/{res-id}/ask-review for non-reviewable')
def act(context):
    #request = APIRequestFactory().post('')
    #force_authenticate(request, context.john)
    #view = ReservationManagementViewSet.as_view(actions={'post': 'ask_review'})
    #context.response = view(request, dorm_pk=context.alfam.id, pk=context.reservation1.id)

    context.reservation1.is_reviewed = True
    context.reservation1.save()
    context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)

    client = APIClient()
    client.force_authenticate(context.john)
    url = reverse('engine.dorms:reservations-ask-review',
                  kwargs={'dorm_pk': context.alfam.id, 'pk': context.reservation1.id})
    context.response = client.post(url)


@then('get 400 Bad Request for reviewing non-reviewable')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST
