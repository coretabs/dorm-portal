from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework import status

from behave import given, when, then

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


@given('we have 2 dormitories with 2 rooms each')
def prepare_dormitory(self):
    create_alfam_dovec_with_4_rooms(self)


@when('serializing alfam to get its all data')
def test_model_can_create_a_message(self):
    self.serialized_dorms = DormDetailsSerializer(
        Dormitory.objects.filter(name='Alfam').superfilter().first())
    self.serialized_dorms_string = str(self.serialized_dorms.data)


@then('get valid serialized alfam data with 2 rooms')
def test_model_can_create_a_message(self):
    # print(self.serialized_dorms_string)
    assert self.serialized_dorms_string.count("'name': 'Alfam'") == 1


@when('hitting GET /dorms/{alfam-id} endpoint')
def prepare_features(self):
    # request = APIRequestFactory().get(reverse('dorms-retrieve'), {'pk': self.alfam.id})
    request = APIRequestFactory().get('')
    view = DormViewSet.as_view(actions={'get': 'retrieve'})
    self.response = view(request, pk=self.alfam.id)


@then('get 200 OK with alfam data')
def test_model_can_create_a_message(self):
    assert self.response.status_code == status.HTTP_200_OK

    filters_keys = self.response.render().data.keys()
    number_of_returned_json_filters = len(list(filters_keys))
    print(self.response.render().data)
    assert number_of_returned_json_filters == 9
