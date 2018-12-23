from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework import status

from behave import given, when, then

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


@given('we have 2 dormitories with 2 rooms each')
def arrange(context):
    create_alfam_dovec_with_4_rooms(context)


@when('serializing alfam to get its all data')
def act(context):
    context.serialized_dorms = DormDetailsSerializer(
        Dormitory.objects.filter(name='Alfam').superfilter().first())
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
    assert number_of_returned_json_filters == 9
