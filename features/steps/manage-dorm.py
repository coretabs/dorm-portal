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


@given('two managers (one for alfam&dovec and one for homedorm)')
def arrange(self):
    self.john = create_manager(self, 'John')
    self.scott = create_manager(self, 'Doe')


@given('we have dorms(alfam & dovec & homedorm) + 2 rooms in alfam')
def arrange(self):
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

    self.options_duration = [RadioOption(name='Spring'), RadioOption(name='Winter')]
    self.duration = create_radio_filter(self.options_duration, 'Duration')
    self.duration_choice_spring = create_radio_choice(self.options_duration[0], self.duration)
    self.duration_choice_winter = create_radio_choice(self.options_duration[1], self.duration)

    self.room_type_options = [RadioOption(name='Single'),
                              RadioOption(name='Double')]
    self.room_types = create_radio_filter(self.room_type_options, 'Room Type')
    self.room_type_single_choice = create_radio_choice(self.room_type_options[0], self.room_types)
    self.room_type_double_choice = create_radio_choice(self.room_type_options[1], self.room_types)

    self.room1 = create_room_with_radio_integral_features(
        self.alfam,
        [self.room_type_single_choice, self.duration_choice_spring],
        [self.price_1000, ],
        [])

    self.room2 = create_room_with_radio_integral_features(
        self.alfam,
        [self.room_type_double_choice, self.duration_choice_winter],
        [self.price_1200, ],
        [])


@when('hitting GET /manager/dorms endpoint')
def act(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.john)
    view = DormManagementViewSet.as_view(actions={'get': 'list'})
    self.response = view(request)


@then('get 200 OK with alfam and dovec')
def test(self):
    assert self.response.status_code == status.HTTP_200_OK

    returned_dorms = self.response.render().data[0]
    # print(self.response.render().data)

    number_of_returned_json_filters = len(list(returned_dorms))
    assert number_of_returned_json_filters == 3

    assert str(self.response.render().data).count("'name', 'Alfam'") == 1
    assert str(self.response.render().data).count("'name', 'Dovec'") == 1


@then('he wont get any other non-owned dorm data')
def test(self):
    assert str(self.response.render().data).count("'name', 'Home Dorm'") == 0


@when('manager asks serializer to bring alfam dorm data')
def act(self):
    self.serialized_dorms = DormManagementDetailsSerializer(self.john.dormitories, many=True)
    self.all_serialized_dorms = str(self.serialized_dorms.data)


@then('get valid serialized alfam data for the manager')
def test(self):
    # print(self.all_serialized_dorms)
    assert self.all_serialized_dorms.count("'name', 'Alfam'") == 1


@when('hitting GET /manager/dorms/{alfam-id}')
def act(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.john)
    view = DormManagementViewSet.as_view(actions={'get': 'retrieve'})
    self.response = view(request, pk=self.alfam.id)


@then('get 200 OK with alfam')
def test(self):
    assert self.response.status_code == status.HTTP_200_OK

    filters_keys = self.response.render().data.keys()
    number_of_returned_json_filters = len(list(filters_keys))
    # print(self.response.render().data)
    assert number_of_returned_json_filters == 13


@when('hitting GET /manager/dorms/{homedorm-id} for non-owned dorm')
def act(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.scott)
    view = DormManagementViewSet.as_view(actions={'get': 'retrieve'})
    self.response = view(request, pk=self.alfam.id)


@then('get forbidden 403 for homedorm')
def test(self):
    assert self.response.status_code == status.HTTP_403_FORBIDDEN


@then('the other manager can get his homedorm')
def test(self):
    request = APIRequestFactory().get('')
    force_authenticate(request, self.scott)
    view = DormManagementViewSet.as_view(actions={'get': 'retrieve'})
    self.response = view(request, pk=self.homedorm.id)

    assert self.response.status_code == status.HTTP_200_OK


@when('deserializing bank data for alfam')
def act(self):
    self.isbank_new_account = {'bank_name': 'isbank',
                               'account_name': 'Faruk', 'account_number': '987654',
                               'swift': 'IN123456', 'iban': 'TR123456', 'currency_code': 'USD'}

    self.deserialized_data = ClientBankAccountSerializer(data=self.isbank_new_account)


@then('validate the deserialized bank data for alfam')
def test(self):
    assert self.deserialized_data.is_valid() == True
    # print(self.deserialized_data)


@when('hitting PUT /manager/dorms/{alfam-id}/bank-accounts/{isbank-id}')
def act(self):
    request = APIRequestFactory().put('', self.isbank_new_account, format='json')
    force_authenticate(request, self.john)
    view = BankAccountManagementViewSet.as_view(actions={'put': 'update'})
    self.response = view(request, dorm_pk=self.alfam.id, pk=self.isbank_alfam_account.id)


@then('get 200 OK for updating alfam isbank data')
def test(self):
    assert self.response.status_code == status.HTTP_200_OK
    assert BankAccount.objects.filter(bank_name='isbank').first().iban == 'TR123456'


@when('hitting same endpoint above to partially update isbank')
def act(self):
    isbank_new_iban = {'iban': '8888888'}

    request = APIRequestFactory().put('', isbank_new_iban, format='json')
    force_authenticate(request, self.john)
    view = BankAccountManagementViewSet.as_view(actions={'put': 'update'})
    self.response = view(request, dorm_pk=self.alfam.id, pk=self.isbank_alfam_account.id)


@then('get 200 OK for partially updating alfam isbank data')
def test(self):
    assert self.response.status_code == status.HTTP_200_OK
    isbank_instance = BankAccount.objects.filter(bank_name='isbank').first()
    assert isbank_instance.iban == '8888888'
    assert isbank_instance.swift == 'IN123456'


@when('hitting POST /manager/dorms/{alfam-id}/bank-accounts')
def act(self):
    ziraat_new_account = {'bank_name': 'ziraat',
                          'account_name': 'Murat', 'account_number': '777777',
                          'swift': 'IN4564181', 'iban': 'TR000000', 'currency_code': 'USD'}

    # print(Currency.objects.all())

    request = APIRequestFactory().post('', ziraat_new_account, format='json')
    force_authenticate(request, self.john)
    view = BankAccountManagementViewSet.as_view(actions={'post': 'create'})
    self.response = view(request, dorm_pk=self.alfam.id)


@then('get 201 CREATED for adding alfam ziraat data')
def test(self):
    # print(self.response.status_code)
    assert self.response.status_code == status.HTTP_201_CREATED
    assert BankAccount.objects.filter(bank_name='ziraat').first().iban == 'TR000000'


@when('hitting DELETE /manager/dorms/{alfam-id}/bank-accounts/{ziraat-id}')
def act(self):
    ziraat = BankAccount.objects.filter(bank_name='ziraat').first()

    request = APIRequestFactory().delete('')
    force_authenticate(request, self.john)
    view = BankAccountManagementViewSet.as_view(actions={'delete': 'destroy'})
    self.response = view(request, dorm_pk=self.alfam.id, pk=ziraat.id)


@then('get 204 NO CONTENT for deleting alfam ziraat bank')
def test(self):
    assert self.response.status_code == status.HTTP_204_NO_CONTENT
    assert BankAccount.objects.filter(bank_name='ziraat').first() == None


@when('hitting POST /manager/dorms/{alfam-id}/photos for non-3d-image')
def act(self):
    uploaded_file = create_uploaded_file(self, 'alfam-photo.jpeg')
    photo_json = {'uploaded_photo': uploaded_file}

    client = APIClient()
    client.force_authenticate(self.john)

    url = reverse('engine.dorms:photos-list', kwargs={'dorm_pk': self.alfam.id})
    self.response = client.post(url, photo_json, format='multipart')


@then('get 201 CREATED for adding alfam photo')
def test(self):
    assert self.response.status_code == status.HTTP_201_CREATED
    assert Dormitory.objects.filter(name='Alfam').first().photos.count() == 1

    assert os.path.exists(self.expected_file_path) == True
    # os.remove(self.expected_file_path)


@when('hitting DELETE /manager/dorms/{alfam-id}/photos/{alfam-photo-id}')
def act(self):
    alfam_photo = Dormitory.objects.filter(name='Alfam').first().photos.first()

    request = APIRequestFactory().delete('')
    force_authenticate(request, self.john)
    view = PhotoDormManagementViewSet.as_view(actions={'delete': 'destroy'})
    self.response = view(request, dorm_pk=self.alfam.id, pk=alfam_photo.id)


@then('delete that photo from alfam')
def test(self):
    assert self.response.status_code == status.HTTP_204_NO_CONTENT
    assert Dormitory.objects.filter(name='Alfam').first().photos.count() == 0
    assert os.path.exists(self.expected_file_path) == False


@when('hitting POST /manager/dorms/{alfam-id}/photos for 3d-image')
def act(self):
    photo_json = {'url': 'https://momento360.com/e/u/a9b53aa8f8b0403ba7a4e18243aabc66', 'is_3d': True}

    client = APIClient()
    client.force_authenticate(self.john)

    url = reverse('engine.dorms:photos-list',
                  kwargs={'dorm_pk': self.alfam.id})
    self.response = client.post(url, photo_json, format='multipart')


@then('get 201 CREATED for adding 3d alfam photo')
def test(self):
    assert self.response.status_code == status.HTTP_201_CREATED
    assert Dormitory.objects.filter(name='Alfam').first().photos.count() == 1


@when('hitting DELETE /manager/dorms/{alfam-id}/photos/{alfam-3d-photo-id}')
def act(self):
    alfam_photo = Dormitory.objects.filter(name='Alfam').first().photos.first()

    request = APIRequestFactory().delete('')
    force_authenticate(request, self.john)
    view = PhotoDormManagementViewSet.as_view(actions={'delete': 'destroy'})
    self.response = view(request, dorm_pk=self.alfam.id, pk=alfam_photo.id)


@then('delete that 3d photo from alfam')
def test(self):
    assert self.response.status_code == status.HTTP_204_NO_CONTENT


@when('deserializing data for updating alfam dorm')
def act(self):
    about_en = {'en': 'Luxury Alfam'}
    about_ar = {'ar': 'الفام الفخيم'}
    about_tr = {'tr': 'Super Alfam'}

    self.updating_alfam_json = {'name': 'Alfam',
                                'abouts': [about_en, about_ar, about_tr],
                                'features': [self.swimming_pool.id, self.free_wifi.id],
                                # 'cover': 'https://images.pexels.com/photos/97904/pexels-photo-97904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
                                'geo_longitude': '35.15010', 'geo_latitude': '33.90111',
                                'address': 'Next to Computer Department',
                                'contact_name': 'Yaser', 'contact_email': 'yaser@gmail.com',
                                'contact_number': '+908501531', 'contact_fax': '+801561561'}

    self.deserialized_data = ClientDormManagementSerializer(data=self.updating_alfam_json)
    print(self.deserialized_data.is_valid())
    print(self.deserialized_data.errors)


@then('validate the deserialized data for updating alfam')
def test(self):
    assert self.deserialized_data.is_valid() == True


@when('hitting PUT /manager/dorms/{alfam-id}')
def act(self):
    request = APIRequestFactory().put('', self.updating_alfam_json, format='json')
    force_authenticate(request, self.john)
    view = DormManagementViewSet.as_view(actions={'put': 'update'})
    self.response = view(request, pk=self.alfam.id)


@then('get 200 OK for updating alfam')
def test(self):
    # print(self.response.data)
    assert self.response.status_code == status.HTTP_200_OK


@when('hitting PUT /manager/dorms/{alfam-id}/cover with new image')
def act(self):
    uploaded_file = create_uploaded_file(self, 'alfam-photo.jpeg')
    cover_json = {'cover': uploaded_file}

    client = APIClient()
    client.force_authenticate(self.john)
    #view = DormManagementViewSet.reverse_action(self, url_name='cover')
    #x = view.reverse_action('update-cover', args=['1'])

    #view = DormManagementViewSet()
    #view.basename = 'engine:dorms'
    #view.request = None

    #url = view.reverse_action('detail-cover', args=['1'])
    url = reverse('engine:manager-dorms-update-cover', kwargs={'pk': self.alfam.id})
    #url = reverse(action, kwargs={'pk': self.alfam.id})

    self.response = client.put(url, cover_json, format='multipart')


@then('get 201 CREATED for adding alfam cover')
def test(self):
    print(self.response.data)
    assert self.response.status_code == status.HTTP_200_OK
    assert Dormitory.objects.filter(name='Alfam').first().cover != None
    assert os.path.exists(self.expected_file_path) == True
    os.remove(self.expected_file_path)
