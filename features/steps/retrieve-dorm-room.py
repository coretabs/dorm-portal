from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework import status

from behave import given, when, then

from freezegun import freeze_time

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


@given('we have 2 dormitories with 2 rooms each')
def arrange(context):
    create_alfam_dovec_with_4_rooms(context)


@given('we have 3 users with reviewable reservations')
def arrange(context):
    context.user1 = create_student(context, 'Owen')
    context.user2 = create_student(context, 'Tia')
    context.user3 = create_student(context, 'Lora')
    context.user4 = create_student(context, 'Putty')
    context.user5 = create_student(context, 'Nina')

    context.reservation1 = create_reservation(context.room1, context.user1)
    context.reservation2 = create_reservation(context.room2, context.user2)
    context.reservation3 = create_reservation(context.room2, context.user3)
    context.reservation4 = create_reservation(context.room2, context.user4)
    context.reservation5 = create_reservation(context.room4, context.user5)

    for reservation in [context.reservation1, context.reservation2,
                        context.reservation3, context.reservation4,
                        context.reservation5]:
        reservation.status = Reservation.CONFIRMED_STATUS
        reservation.save()


@given('we have 3 reviews of 4.5, 5.0, 2.2, 1.0')
def arrange(context):

    with freeze_time(context.reservation2.reservation_creation_date + datetime.timedelta(days=90)):
        context.reservation1.create_review(stars=4.5, description='it was a bit good')

    with freeze_time(context.reservation2.reservation_creation_date + datetime.timedelta(days=91)):
        context.reservation2.create_review(stars=5.0, description='super super super')
        context.reservation3.create_review(stars=2.2, description='stupid')
        context.reservation4.create_review(stars=1.0, description='bad bad bad')
        context.reservation5.create_review(stars=0.0, description='worst place ever')


@when('asking for last 3 reviews')
def act(context):
    context.alfam_with_three_reviews = Dormitory.objects.filter(name='Alfam')\
                                                        .superfilter().with_last_3_reviews().first()


@then('get last 3 reviews without the first 4.5')
def test(context):
    reviews = context.alfam_with_three_reviews.reviews
    # print(reviews.all())
    assert reviews.count() == 3
    assert reviews.filter(stars=4.5).count() == 0


@when('asking for reviews statistics')
def act(context):
    context.alfam_with_statsitics = Dormitory.objects.filter(name='Alfam')\
        .superfilter().with_reviews_statistics().first()


@then('get 4 reviews and 3.175 avg rating')
def test(context):
    assert context.alfam_with_statsitics.number_of_reviews == 4
    assert context.alfam_with_statsitics.stars_average == 3.175


@when('serializing alfam to get its all data')
def act(context):
    context.serialized_dorms = DormDetailsSerializer(
        Dormitory.objects.filter(name='Alfam').superfilter().with_last_3_reviews().with_reviews_statistics().first())
    context.serialized_dorms_string = str(context.serialized_dorms.data)


@then('get valid serialized alfam data with 2 rooms')
def test(context):
    # print(context.serialized_dorms_string)
    assert context.serialized_dorms_string.count("'name': 'Alfam'") == 1


@when('hitting GET /dorms/{alfam-id} endpoint')
def act(context):
    # request = APIRequestFactory().get(reverse('dorms-retrieve'), {'pk': context.alfam.id})
    request = APIRequestFactory().get('')
    view = DormViewSet.as_view(actions={'get': 'retrieve'})
    context.response = view(request, pk=context.alfam.id)


@then('get 200 OK with alfam data')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK

    filters_keys = context.response.render().data.keys()
    number_of_returned_json_filters = len(list(filters_keys))
    print(context.response.render().data)
    print(number_of_returned_json_filters)
    assert number_of_returned_json_filters == 12
