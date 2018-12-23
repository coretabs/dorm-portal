import os

from django.urls import reverse
from django.contrib.sites.models import Site
from django.core import mail
from django.conf import settings
from django.test.utils import override_settings

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
def act(self):
    self.reservation1.status = Reservation.PENDING_STATUS
    self.reservation2.status = Reservation.PENDING_STATUS
    self.reservation1.save()
    self.reservation2.save()


@then('is_reviewable is false for non-confirmed reservations')
def test(self):
    self.reservation1 = Reservation.objects.get(pk=self.reservation1.id)
    self.reservation2 = Reservation.objects.get(pk=self.reservation2.id)
    assert self.reservation1.is_reviewable == False
    assert self.reservation2.is_reviewable == False


@when('reservation is confirmed and after three months')
def act(self):
    self.reservation1.status = Reservation.CONFIRMED_STATUS
    self.reservation2.status = Reservation.CONFIRMED_STATUS

    self.reservation1.save()
    self.reservation2.save()


@then('is_reviewable is true for confirmed past 3 months reservation')
def test(self):
    self.reservation_creation_date_plus_three_months = self.reservation2.reservation_creation_date + \
        datetime.timedelta(days=90)

    with freeze_time(self.reservation_creation_date_plus_three_months):
        self.reservation1 = Reservation.objects.get(pk=self.reservation1.id)
        self.reservation2 = Reservation.objects.get(pk=self.reservation2.id)
        # print(datetime.date.today())
        assert self.reservation1.is_reviewable == True
        assert self.reservation2.is_reviewable == True


@when('reservation is confirmed and before three months')
def act(self):
    self.reservation1.status = Reservation.CONFIRMED_STATUS
    self.reservation2.status = Reservation.CONFIRMED_STATUS

    self.reservation1.save()
    self.reservation2.save()


@then('is_reviewable is false for confirmed less 3 months reservation')
def test(self):
    self.reservation_creation_date_plus_two_months = self.reservation2.reservation_creation_date + \
        datetime.timedelta(days=60)

    with freeze_time(self.reservation_creation_date_plus_two_months):
        self.reservation1 = Reservation.objects.get(pk=self.reservation1.id)
        self.reservation2 = Reservation.objects.get(pk=self.reservation2.id)
        # print(datetime.date.today())
        assert self.reservation1.is_reviewable == False
        assert self.reservation2.is_reviewable == False


@when('reservation is already reviewed')
def act(self):
    self.reservation1.is_reviewed = True
    self.reservation2.is_reviewed = False

    self.reservation1.save()
    self.reservation2.save()


@then('is_reviewable is false for already reviewed reservation')
def test(self):
    self.reservation_creation_date_plus_two_months = self.reservation2.reservation_creation_date + \
        datetime.timedelta(days=90)

    with freeze_time(self.reservation_creation_date_plus_two_months):
        self.reservation1 = Reservation.objects.get(pk=self.reservation1.id)
        self.reservation2 = Reservation.objects.get(pk=self.reservation2.id)
        # print(datetime.date.today())
        assert self.reservation1.is_reviewable == False
        assert self.reservation2.is_reviewable == True


@then('return the first reservation is_reviewed into false')
def test(self):
    self.reservation1.is_reviewed = False
    self.reservation1.save()
    self.reservation1 = Reservation.objects.get(pk=self.reservation1.id)


@when('asking for review and saving')
def act(self):
    site = Site(domain='http://127.0.0.1:8000', name='127.0.0.1')
    site.save()

    request = {'SITE_ID': site.id}
    self.asking_reservation = {'reservation_id': self.reservation1.id}
    self.deserialized_data = AskForReviewSerializer(
        data=self.asking_reservation, context={'request': request})


@then('validate data and send email for review asking')
def test(self):
    with freeze_time(self.reservation_creation_date_plus_two_months):
        assert self.deserialized_data.is_valid() == True
        assert len(mail.outbox) == 0

        self.deserialized_data.save()
        #assert len(mail.outbox) == 1


@when('hitting POST /manager/dorms/{alfam-id}/reservations/{res-id}/ask-review')
@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
def act(self):
    #request = APIRequestFactory().post('')
    #force_authenticate(request, self.john)
    #view = ReservationManagementViewSet.as_view(actions={'post': 'ask_review'})
    #self.response = view(request, dorm_pk=self.alfam.id, pk=self.reservation1.id)
    with freeze_time(self.reservation_creation_date_plus_two_months):
        client = APIClient()
        client.force_authenticate(self.john)
        url = reverse('engine.dorms:reservations-ask-review',
                      kwargs={'dorm_pk': self.alfam.id, 'pk': self.reservation1.id})
        self.response = client.post(url)
        print(len(mail.outbox))


@then('get 200 OK for sending review email')
def test(self):
    # print(self.response.status_code)
    assert self.response.status_code == status.HTTP_200_OK


@when('hitting POST /manager/dorms/{alfam-id}/reservations/{res-id}/ask-review for non-reviewable')
def act(self):
    #request = APIRequestFactory().post('')
    #force_authenticate(request, self.john)
    #view = ReservationManagementViewSet.as_view(actions={'post': 'ask_review'})
    #self.response = view(request, dorm_pk=self.alfam.id, pk=self.reservation1.id)

    self.reservation1.is_reviewed = True
    self.reservation1.save()
    self.reservation1 = Reservation.objects.get(pk=self.reservation1.id)

    client = APIClient()
    client.force_authenticate(self.john)
    url = reverse('engine.dorms:reservations-ask-review',
                  kwargs={'dorm_pk': self.alfam.id, 'pk': self.reservation1.id})
    self.response = client.post(url)


@then('get 400 Bad Request for reviewing non-reviewable')
def test(self):
    # print(self.response.status_code)
    assert self.response.status_code == status.HTTP_400_BAD_REQUEST
