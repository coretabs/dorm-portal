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
    context.reservation_creation_date_plus_three_months = context.reservation2.reservation_creation_date + \
        datetime.timedelta(days=90)

    with freeze_time(context.reservation_creation_date_plus_three_months):
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

    with freeze_time(context.reservation_creation_date_plus_three_months):
        assert context.deserialized_data.is_valid() == True
        assert len(mail.outbox) == 0

        context.deserialized_data.save()
        assert len(mail.outbox) == 1


@when('hitting POST /manager-dorms/{alfam-id}/reservations/{res-id}/ask-review')
def act(context):
    #request = APIRequestFactory().post('')
    #force_authenticate(request, context.john)
    #view = ReservationManagementViewSet.as_view(actions={'post': 'ask_review'})
    #context.response = view(request, dorm_pk=context.alfam.id, pk=context.reservation1.id)
    with freeze_time(context.reservation_creation_date_plus_three_months):
        client = APIClient()
        client.force_authenticate(context.john)
        url = reverse('engine.manager-dorms:reservations-ask-review',
                      kwargs={'dorm_pk': context.alfam.id, 'pk': context.reservation1.id})
        context.response = client.post(url)
        print(len(mail.outbox))


@then('get 200 OK for sending review email')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_200_OK
    assert len(mail.outbox) == 2


@when('hitting POST /manager-dorms/{alfam-id}/reservations/{res-id}/ask-review for non-reviewable')
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
    url = reverse('engine.manager-dorms:reservations-ask-review',
                  kwargs={'dorm_pk': context.alfam.id, 'pk': context.reservation1.id})
    context.response = client.post(url)


@then('get 400 Bad Request for reviewing non-reviewable')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST


@when('creating a review for a reservation')
def act(context):
    context.reservation1.is_reviewed = False
    context.reservation1.status = Reservation.CONFIRMED_STATUS
    context.reservation1.save()
    context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)

    context.reservation_creation_date_plus_three_months =\
        context.reservation1.reservation_creation_date + datetime.timedelta(days=90)

    with freeze_time(context.reservation_creation_date_plus_three_months):
        assert context.reservation1.is_reviewed == False
        context.reservation1.create_review(stars=5.0, description='It was soooo bad !')


@then('reservation is_reviewed should be True')
def test(context):
    context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)
    assert context.reservation1.is_reviewed == True


@when('creating a review for is_reviewable=False reservation')
def act(context):
    context.reservation1.is_reviewed = True
    context.reservation1.save()
    context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)

    with freeze_time(context.reservation_creation_date_plus_three_months):
        try:
            assert context.reservation1.is_reviewable == False
            context.reservation1.create_review(stars=5.0, description='It was soooo bad !')
            context.result_exception = None
        except Exception as e:
            context.result_exception = e


@then('creating review throws NonReviewableReservation')
def test(context):
    assert context.result_exception != None
    assert isinstance(context.result_exception, NonReviewableReservation) == True


@when('serializing dorm reviews')
def act(context):
    context.serialized_reviews = ReviewSerializer(context.alfam.reviews, many=True)
    context.all_serialized_reviews = str(context.serialized_reviews.data)


@then('get valid serialized dorm reviews')
def test(context):
    # print(context.all_serialized_reviews)
    assert context.all_serialized_reviews.count("'stars', '5.0'") == 1


@when('hitting GET /dorm/{alfam-id}/reviews')
def act(context):
    request = APIRequestFactory().get('')
    view = DormViewSet.as_view(actions={'get': 'reviews'})
    context.response = view(request, pk=context.alfam.id)


@then('get 200 OK with alfam reviews')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    assert str(context.response.render().data).count("'stars', '5.0'") == 1


@when('deserializing dorm review sent by user')
def act(context):
    context.review_json = {'stars': '3',
                           'description': 'I didnt like it!'}

    context.deserializer = ReviewSerializer(data=context.review_json,
                                            context={'reservation_id': context.reservation1.id})


@then('get validated deserialized review')
def test(context):
    assert context.deserializer.is_valid() == True
    # print(context.deserialized_data)


@then('save that review successfully')
def test(context):
    Review.objects.all().delete()
    assert Review.objects.count() == 0

    context.reservation1.is_reviewed = False
    context.reservation1.status = Reservation.CONFIRMED_STATUS
    context.reservation1.save()
    context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)

    with freeze_time(context.reservation_creation_date_plus_three_months):
        context.deserializer.save()
        assert Review.objects.count() == 1


@when('hitting POST /reservations/{res-id}/reviews')
def act(context):
    Review.objects.all().delete()
    assert Review.objects.count() == 0

    context.reservation1.is_reviewed = False
    context.reservation1.status = Reservation.CONFIRMED_STATUS
    context.reservation1.save()
    context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)

    with freeze_time(context.reservation_creation_date_plus_three_months):
        request = APIRequestFactory().post('', context.review_json, format='json')
        force_authenticate(request, context.user1)
        view = ReservationViewSet.as_view(actions={'post': 'add_review'})
        context.response = view(request, pk=context.reservation1.id)


@then('get 201 Created for creating the review')
def test(context):
    assert context.response.status_code == status.HTTP_201_CREATED
    assert Review.objects.count() == 1


@when('hitting POST /reservations/{res-id}/reviews for non-reviewable dorm')
def act(context):
    Review.objects.all().delete()
    assert Review.objects.count() == 0

    context.reservation1.is_reviewed = True
    context.reservation1.status = Reservation.CONFIRMED_STATUS
    context.reservation1.save()
    context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)

    with freeze_time(context.reservation_creation_date_plus_three_months):
        request = APIRequestFactory().post('', context.review_json, format='json')
        force_authenticate(request, context.user1)
        view = ReservationViewSet.as_view(actions={'post': 'add_review'})
        context.response = view(request, pk=context.reservation1.id)


@then('get 400 Bad Request for not creating the review')
def test(context):
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST
    assert Review.objects.count() == 0


@when('hitting POST /reservations/{res-id}/reviews for non-owned reservation')
def act(context):
    Review.objects.all().delete()
    assert Review.objects.count() == 0

    context.reservation1.is_reviewed = False
    context.reservation1.status = Reservation.CONFIRMED_STATUS
    context.reservation1.save()
    context.reservation1 = Reservation.objects.get(pk=context.reservation1.id)

    with freeze_time(context.reservation_creation_date_plus_three_months):
        request = APIRequestFactory().post('', context.review_json, format='json')
        force_authenticate(request, context.user2)
        view = ReservationViewSet.as_view(actions={'post': 'add_review'})
        context.response = view(request, pk=context.reservation1.id)


@then('get 403 forbidden for not creating the review')
def test(context):
    assert context.response.status_code == status.HTTP_403_FORBIDDEN
    assert Review.objects.count() == 0
