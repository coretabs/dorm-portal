import os

from django.urls import reverse
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
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

    self.swimming_pool = create_dorm_feature('Swimming pool')
    self.free_wifi = create_dorm_feature('Free WiFi')

    self.alfam = create_dorm('Alfam', self.category_public, manager=self.john)
    self.dovec = create_dorm('Dovec', self.category_private, manager=self.john)
    self.homedorm = create_dorm('Home Dorm', self.category_private, manager=self.scott)

    self.alfam.about = LazyI18nString(
        {'ar': 'الفام العظيم', 'tr': 'Harika Alfam', 'en': 'Great Alfam'})

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
    # print(self.response.render().data)
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


@when('deserializing bank data for alfam')
def filtering(self):
    self.isbank_new_account = {'bank_name': 'isbank',
                               'account_name': 'Faruk', 'account_number': '987654',
                               'swift': 'IN123456', 'iban': 'TR123456', 'currency_code': 'USD'}

    self.deserialized_data = ClientBankAccountSerializer(data=self.isbank_new_account)


@then('validate the deserialized bank data for alfam')
def test_model_can_create_a_message(self):
    assert self.deserialized_data.is_valid() == True
    # print(self.deserialized_data)


@when('hitting PUT /manager/dorms/{alfam-id}/bank-accounts/{isbank-id}')
def filtering(self):
    request = APIRequestFactory().put('', self.isbank_new_account, format='json')
    force_authenticate(request, self.john)
    view = BankAccountManagementViewSet.as_view(actions={'put': 'update'})
    self.response = view(request, dorm_pk=self.alfam.id, pk=self.isbank_alfam_account.id)


@then('get 200 OK and for updating alfam isbank data')
def test_model_can_create_a_message(self):
    assert self.response.status_code == status.HTTP_200_OK
    assert BankAccount.objects.filter(bank_name='isbank').first().iban == 'TR123456'


@when('hitting same endpoint above to partially update isbank')
def filtering(self):
    isbank_new_iban = {'iban': '8888888'}

    request = APIRequestFactory().put('', isbank_new_iban, format='json')
    force_authenticate(request, self.john)
    view = BankAccountManagementViewSet.as_view(actions={'put': 'update'})
    self.response = view(request, dorm_pk=self.alfam.id, pk=self.isbank_alfam_account.id)


@then('get 200 OK and for partially updating alfam isbank data')
def test_model_can_create_a_message(self):
    assert self.response.status_code == status.HTTP_200_OK
    isbank_instance = BankAccount.objects.filter(bank_name='isbank').first()
    assert isbank_instance.iban == '8888888'
    assert isbank_instance.swift == 'IN123456'


@when('hitting POST /manager/dorms/{alfam-id}/bank-accounts')
def filtering(self):
    ziraat_new_account = {'bank_name': 'ziraat',
                          'account_name': 'Murat', 'account_number': '777777',
                          'swift': 'IN4564181', 'iban': 'TR000000', 'currency_code': 'USD'}

    # print(Currency.objects.all())

    request = APIRequestFactory().post('', ziraat_new_account, format='json')
    force_authenticate(request, self.john)
    view = BankAccountManagementViewSet.as_view(actions={'post': 'create'})
    self.response = view(request, dorm_pk=self.alfam.id)


@then('get 201 CREATED and for adding alfam ziraat data')
def test_model_can_create_a_message(self):
    # print(self.response.status_code)
    assert self.response.status_code == status.HTTP_201_CREATED
    assert BankAccount.objects.filter(bank_name='ziraat').first().iban == 'TR000000'


@when('hitting POST DELETE /manager/dorms/{alfam-id}/bank-accounts/{ziraat-id}')
def filtering(self):
    ziraat = BankAccount.objects.filter(bank_name='ziraat').first()

    request = APIRequestFactory().delete('')
    force_authenticate(request, self.john)
    view = BankAccountManagementViewSet.as_view(actions={'delete': 'destroy'})
    self.response = view(request, dorm_pk=self.alfam.id, pk=ziraat.id)


@then('get 204 NO CONTENT and for deleting alfam ziraat bank')
def test_model_can_create_a_message(self):
    assert self.response.status_code == status.HTTP_204_NO_CONTENT
    assert BankAccount.objects.filter(bank_name='ziraat').first() == None


@when('hitting POST /manager/dorms/{alfam-id}/photos')
def filtering(self):
    self.expected_file_path = os.path.join(settings.MEDIA_ROOT, 'alfam-photo.jpeg')
    if os.path.exists(self.expected_file_path):
        os.remove(self.expected_file_path)

    photo_file = File(open(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'alfam-photo.jpeg'), 'rb'))

    uploaded_file = SimpleUploadedFile('alfam-photo.jpeg', photo_file.read(),
                                       content_type='multipart/form-data')
    photo_json = {'uploaded_photo': uploaded_file}

    client = APIClient()
    client.force_authenticate(self.john)

    url = reverse('photos-list',
                  kwargs={'dorm_pk': self.alfam.id})
    self.response = client.post(url, photo_json, format='multipart')
    # view = PhotoDormManagementViewSet.as_view(actions={'post': 'create'})

    # = view(request, dorm_pk=self.alfam.id)


@then('get 201 CREATED and for adding alfam photo')
def test_model_can_create_a_message(self):
    assert self.response.status_code == status.HTTP_201_CREATED
    assert Dormitory.objects.filter(name='Alfam').first().photos.count() == 1

    assert os.path.exists(self.expected_file_path) == True
    os.remove(self.expected_file_path)


@when('deserializing data for updating alfam dorm')
def filtering(self):
    about_en = {'lang_code': 'en', 'about': 'Luxury Alfam'}
    about_ar = {'lang_code': 'ar', 'about': 'الفام الفخيم'}
    about_tr = {'lang_code': 'tr', 'about': 'Super Alfam'}

    feature_swimming_pool = {'id': self.swimming_pool.id, }
    feature_free_wifi = {'id': self.free_wifi.id, }

    # photo1 =

    self.updating_json_data = {'name': 'Alfama',
                               'about': [about_en, about_ar, about_tr],
                               'features': [feature_free_wifi, feature_swimming_pool],
                               'cover': 'https://images.pexels.com/photos/97904/pexels-photo-97904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
                               # 'photos': [photo1, photo2],
                               'geo_longitude': '35.15010', 'geo_latitude': '33.90111', 'address': 'Next to Computer Department',
                               'contact_name': 'Yaser', 'contact_email': 'yaser@gmail.com', 'contact_number': '+908501531', 'contact_fax': '+801561561'}

    self.deserialized_data = ClientAcceptedFiltersSerializer(data=self.updating_json_data)


@then('validate the deserialized data for updating alfam')
def test_model_can_create_a_message(self):
    assert self.deserialized_data.is_valid() == True
