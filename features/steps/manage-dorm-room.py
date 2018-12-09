from django.urls import reverse

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from behave import given, when, then

from i18nfield.strings import LazyI18nString

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


@given('two managers (one for alfam&dovec and one for homedorm)')
def prepare_dormitory(self):
    self.john = create_manager(self, 'John')
    self.scott = create_manager(self, 'Doe')


@given('we have dorms(alfam & dovec & homedorm) + 2 rooms in alfam')
def filtering(self):
    self.category_public = create_category('public')
    self.category_private = create_category('private')

    self.alfam = create_dorm('Alfam', self.category_public, manager=self.john)
    self.dovec = create_dorm('Dovec', self.category_private, manager=self.john)
    self.homedorm = create_dorm('Home Dorm', self.category_private, manager=self.scott)

    self.alfam.about = LazyI18nString(
        {'ar': 'الفام العظيم', 'tr': 'Super Alfam', 'en': 'Great Alfam'})

    self.usd = create_currency('$', 'USD')
    self.isbank_alfam_account = create_bank_account('isbank', '123456', self.usd, self.alfam)

    self.alfam.save()

    self.price_filter = IntegralFilter(name='Price')
    self.price_filter.save()
    self.price_1000 = create_integral_choice(self.price_filter, 1000)
    self.price_1200 = create_integral_choice(self.price_filter, 1200)

    self.room_type_options = [RadioOption(name='Single'),
                              RadioOption(name='Double')]
    self.room_types = create_radio_filter(self.room_type_options, 'Room Type')
    self.room_type_single_choice = create_radio_choice(self.room_type_options[0], self.room_types)
    self.room_type_double_choice = create_radio_choice(self.room_type_options[1], self.room_types)

    self.room1 = create_room_with_radio_integral_features(
        self.alfam,
        [self.room_type_single_choice, ],
        [self.price_1000, ],
        [])

    self.room2 = create_room_with_radio_integral_features(
        self.alfam,
        [self.room_type_double_choice, ],
        [self.price_1200, ],
        [])


@when('hitting GET /manager/dorms endpoint')
def filtering(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.john)
    view = DormManagementViewSet.as_view(actions={'get': 'list'})
    self.response = view(request)


@then('get 200 OK with alfam and dovec')
def test_model_can_create_a_message(self):
    assert self.response.status_code == status.HTTP_200_OK

    returned_dorms = self.response.render().data[0]
    # print(self.response.render().data)

    number_of_returned_json_filters = len(list(returned_dorms))
    assert number_of_returned_json_filters == 3

    assert str(self.response.render().data).count("'name', 'Alfam'") == 1
    assert str(self.response.render().data).count("'name', 'Dovec'") == 1


@then('he wont get any other non-owned dorm data')
def test_model_can_create_a_message(self):
    assert str(self.response.render().data).count("'name', 'Home Dorm'") == 0


@when('manager asks serializer to bring alfam dorm data')
def filtering(self):
    self.serialized_dorms = DormManagementDetailsSerializer(self.john.dormitories, many=True)
    self.all_serialized_dorms = str(self.serialized_dorms.data)


@then('get valid serialized alfam data for the manager')
def test_model_can_create_a_message(self):
    # print(self.all_serialized_dorms)
    assert self.all_serialized_dorms.count("'name', 'Alfam'") == 1


@when('hitting GET /manager/dorms/{alfam-id}')
def filtering(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.john)
    view = DormManagementViewSet.as_view(actions={'get': 'retrieve'})
    self.response = view(request, pk=self.alfam.id)


@then('get 200 OK with alfam')
def test_model_can_create_a_message(self):
    assert self.response.status_code == status.HTTP_200_OK

    filters_keys = self.response.render().data.keys()
    number_of_returned_json_filters = len(list(filters_keys))
    print(self.response.render().data)
    assert number_of_returned_json_filters == 13


@when('hitting GET /manager/dorms/{homedorm-id} for non-owned dorm')
def filtering(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.scott)
    view = DormManagementViewSet.as_view(actions={'get': 'retrieve'})
    self.response = view(request, pk=self.alfam.id)


@then('get forbidden 403 for homedorm')
def test_model_can_create_a_message(self):
    assert self.response.status_code == status.HTTP_403_FORBIDDEN


@then('the other manager can get his homedorm')
def test_model_can_create_a_message(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.scott)
    view = DormManagementViewSet.as_view(actions={'get': 'retrieve'})
    self.response = view(request, pk=self.homedorm.id)

    assert self.response.status_code == status.HTTP_200_OK
