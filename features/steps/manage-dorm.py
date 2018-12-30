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
def arrange(context):
    context.john = create_manager(context, 'John')
    context.scott = create_manager(context, 'Scott')


@given('we have dorms(alfam & dovec & homedorm) + 2 rooms in alfam')
def arrange(context):
    context.category_public = create_category('public')
    context.category_private = create_category('private')

    context.swimming_pool = create_dorm_feature('Swimming pool')
    context.free_wifi = create_dorm_feature('Free WiFi')

    context.alfam = create_dorm('Alfam', context.category_public, manager=context.john)
    context.dovec = create_dorm('Dovec', context.category_private, manager=context.john)
    context.homedorm = create_dorm('Home Dorm', context.category_private, manager=context.scott)

    context.alfam.about = LazyI18nString(
        {'ar': 'الفام العظيم', 'tr': 'Harika Alfam', 'en': 'Great Alfam'})

    context.usd = create_currency('$', 'USD')
    context.isbank_alfam_account = create_bank_account(
        'isbank', '123456', context.usd, context.alfam)

    context.alfam.save()

    context.price_filter = IntegralFilter(name='Price')
    context.price_filter.save()
    context.price_1000 = create_integral_choice(context.price_filter, 1000)
    context.price_1200 = create_integral_choice(context.price_filter, 1200)

    context.options_duration = [RadioOption(name='Spring'), RadioOption(name='Winter')]
    context.duration = create_radio_filter(context.options_duration, 'Duration')
    context.duration_choice_spring = create_radio_choice(
        context.options_duration[0], context.duration)
    context.duration_choice_winter = create_radio_choice(
        context.options_duration[1], context.duration)

    context.room_type_options = [RadioOption(name='Single'),
                                 RadioOption(name='Double')]
    context.room_types = create_radio_filter(context.room_type_options, 'Room Type')
    context.room_type_single_choice = create_radio_choice(
        context.room_type_options[0], context.room_types)
    context.room_type_double_choice = create_radio_choice(
        context.room_type_options[1], context.room_types)

    context.people_allowed_number_filter = IntegralFilter(name=LazyI18nString(
        {'tr': 'Kişi İzin Numarası', 'en': 'People Allowed Number'}))
    context.people_allowed_number_filter.save()
    context.one_person = create_integral_choice(context.people_allowed_number_filter, 1)
    context.two_persons = create_integral_choice(context.people_allowed_number_filter, 2)

    context.room1 = create_room_with_radio_integral_features(
        context.alfam,
        [context.room_type_single_choice, context.duration_choice_spring],
        [context.price_1000, context.one_person],
        [])

    context.room2 = create_room_with_radio_integral_features(
        context.alfam,
        [context.room_type_double_choice, context.duration_choice_winter],
        [context.price_1200, context.two_persons],
        [])


@when('hitting GET /manager/dorms endpoint')
def act(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.john)
    view = DormManagementViewSet.as_view(actions={'get': 'list'})
    context.response = view(request)


@then('get 200 OK with alfam and dovec')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK

    returned_dorms = context.response.render().data[0]
    # print(context.response.render().data)

    number_of_returned_json_filters = len(list(returned_dorms))
    assert number_of_returned_json_filters == 3

    assert str(context.response.render().data).count("'name', 'Alfam'") == 1
    assert str(context.response.render().data).count("'name', 'Dovec'") == 1


@then('he wont get any other non-owned dorm data')
def test(context):
    assert str(context.response.render().data).count("'name', 'Home Dorm'") == 0


@when('manager asks serializer to bring alfam dorm data')
def act(context):
    context.serialized_dorms = DormManagementDetailsSerializer(context.john.dormitories, many=True)
    context.all_serialized_dorms = str(context.serialized_dorms.data)


@then('get valid serialized alfam data for the manager')
def test(context):
    # print(context.all_serialized_dorms)
    assert context.all_serialized_dorms.count("'name', 'Alfam'") == 1


@when('hitting GET /manager-dorms/{alfam-id}')
def act(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.john)
    view = DormManagementViewSet.as_view(actions={'get': 'retrieve'})
    context.response = view(request, pk=context.alfam.id)


@then('get 200 OK with alfam')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK

    filters_keys = context.response.render().data.keys()
    number_of_returned_json_filters = len(list(filters_keys))
    # print(context.response.render().data)
    assert number_of_returned_json_filters == 14


@when('hitting GET /manager-dorms/{homedorm-id} for non-owned dorm')
def act(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.scott)
    view = DormManagementViewSet.as_view(actions={'get': 'retrieve'})
    context.response = view(request, pk=context.alfam.id)


@then('get forbidden 403 for homedorm')
def test(context):
    assert context.response.status_code == status.HTTP_403_FORBIDDEN


@then('the other manager can get his homedorm')
def test(context):
    request = APIRequestFactory().get('')
    force_authenticate(request, context.scott)
    view = DormManagementViewSet.as_view(actions={'get': 'retrieve'})
    context.response = view(request, pk=context.homedorm.id)

    assert context.response.status_code == status.HTTP_200_OK


@when('deserializing bank data for alfam')
def act(context):
    context.isbank_new_account = {'bank_name': 'isbank',
                                  'account_name': 'Faruk', 'account_number': '987654',
                                  'swift': 'IN123456', 'iban': 'TR123456', 'currency_code': 'USD'}

    context.deserialized_data = ClientBankAccountSerializer(data=context.isbank_new_account)


@then('validate the deserialized bank data for alfam')
def test(context):
    assert context.deserialized_data.is_valid() == True
    # print(context.deserialized_data)


@when('hitting PUT /manager-dorms/{alfam-id}/bank-accounts/{isbank-id}')
def act(context):
    request = APIRequestFactory().put('', context.isbank_new_account, format='json')
    force_authenticate(request, context.john)
    view = BankAccountManagementViewSet.as_view(actions={'put': 'update'})
    context.response = view(request, dorm_pk=context.alfam.id, pk=context.isbank_alfam_account.id)


@then('get 200 OK for updating alfam isbank data')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    assert BankAccount.objects.filter(bank_name='isbank').first().iban == 'TR123456'


@when('hitting same endpoint above to partially update isbank')
def act(context):
    isbank_new_iban = {'iban': '8888888'}

    request = APIRequestFactory().put('', isbank_new_iban, format='json')
    force_authenticate(request, context.john)
    view = BankAccountManagementViewSet.as_view(actions={'put': 'update'})
    context.response = view(request, dorm_pk=context.alfam.id, pk=context.isbank_alfam_account.id)


@then('get 200 OK for partially updating alfam isbank data')
def test(context):
    assert context.response.status_code == status.HTTP_200_OK
    isbank_instance = BankAccount.objects.filter(bank_name='isbank').first()
    assert isbank_instance.iban == '8888888'
    assert isbank_instance.swift == 'IN123456'


@when('hitting POST /manager-dorms/{alfam-id}/bank-accounts')
def act(context):
    ziraat_new_account = {'bank_name': 'ziraat',
                          'account_name': 'Murat', 'account_number': '777777',
                          'swift': 'IN4564181', 'iban': 'TR000000', 'currency_code': 'USD'}

    # print(Currency.objects.all())

    request = APIRequestFactory().post('', ziraat_new_account, format='json')
    force_authenticate(request, context.john)
    view = BankAccountManagementViewSet.as_view(actions={'post': 'create'})
    context.response = view(request, dorm_pk=context.alfam.id)


@then('get 201 CREATED for adding alfam ziraat data')
def test(context):
    # print(context.response.status_code)
    assert context.response.status_code == status.HTTP_201_CREATED
    assert BankAccount.objects.filter(bank_name='ziraat').first().iban == 'TR000000'


@when('hitting DELETE /manager-dorms/{alfam-id}/bank-accounts/{ziraat-id}')
def act(context):
    ziraat = BankAccount.objects.filter(bank_name='ziraat').first()

    request = APIRequestFactory().delete('')
    force_authenticate(request, context.john)
    view = BankAccountManagementViewSet.as_view(actions={'delete': 'destroy'})
    context.response = view(request, dorm_pk=context.alfam.id, pk=ziraat.id)


@then('get 204 NO CONTENT for deleting alfam ziraat bank')
def test(context):
    assert context.response.status_code == status.HTTP_204_NO_CONTENT
    assert BankAccount.objects.filter(bank_name='ziraat').first() == None


@when('hitting POST /manager-dorms/{alfam-id}/photos for non-3d-image')
def act(context):
    uploaded_file = create_uploaded_file(context, 'alfam-photo.jpeg')
    photo_json = {'uploaded_photo': uploaded_file}

    client = APIClient()
    client.force_authenticate(context.john)

    url = reverse('engine.manager-dorms:photos-list', kwargs={'dorm_pk': context.alfam.id})
    context.response = client.post(url, photo_json, format='multipart')


@then('get 201 CREATED for adding alfam photo')
def test(context):
    assert context.response.status_code == status.HTTP_201_CREATED
    assert Dormitory.objects.filter(name='Alfam').first().photos.count() == 1

    assert os.path.exists(context.expected_file_path) == True
    # os.remove(context.expected_file_path)


@when('hitting DELETE /manager-dorms/{alfam-id}/photos/{alfam-photo-id}')
def act(context):
    alfam_photo = Dormitory.objects.filter(name='Alfam').first().photos.first()

    request = APIRequestFactory().delete('')
    force_authenticate(request, context.john)
    view = PhotoDormManagementViewSet.as_view(actions={'delete': 'destroy'})
    context.response = view(request, dorm_pk=context.alfam.id, pk=alfam_photo.id)


@then('delete that photo from alfam')
def test(context):
    assert context.response.status_code == status.HTTP_204_NO_CONTENT
    assert Dormitory.objects.filter(name='Alfam').first().photos.count() == 0
    assert os.path.exists(context.expected_file_path) == False


@when('hitting POST /manager-dorms/{alfam-id}/photos for 3d-image')
def act(context):
    photo_json = {'url': 'https://momento360.com/e/u/a9b53aa8f8b0403ba7a4e18243aabc66', 'is_3d': True}

    client = APIClient()
    client.force_authenticate(context.john)

    url = reverse('engine.manager-dorms:photos-list',
                  kwargs={'dorm_pk': context.alfam.id})
    context.response = client.post(url, photo_json, format='multipart')


@then('get 201 CREATED for adding 3d alfam photo')
def test(context):
    assert context.response.status_code == status.HTTP_201_CREATED
    assert Dormitory.objects.filter(name='Alfam').first().photos.count() == 1

    assert Dormitory.objects.filter(name='Alfam').first()\
        .photos.first().url == 'https://momento360.com/e/u/a9b53aa8f8b0403ba7a4e18243aabc66'


@when('hitting DELETE /manager-dorms/{alfam-id}/photos/{alfam-3d-photo-id}')
def act(context):
    alfam_photo = Dormitory.objects.filter(name='Alfam').first().photos.first()

    request = APIRequestFactory().delete('')
    force_authenticate(request, context.john)
    view = PhotoDormManagementViewSet.as_view(actions={'delete': 'destroy'})
    context.response = view(request, dorm_pk=context.alfam.id, pk=alfam_photo.id)


@then('delete that 3d photo from alfam')
def test(context):
    assert context.response.status_code == status.HTTP_204_NO_CONTENT


@when('deserializing data for updating alfam dorm')
def act(context):
    about_en = {'en': 'Luxury Alfam'}
    about_ar = {'ar': 'الفام الفخيم'}
    about_tr = {'tr': 'Super Alfam'}

    context.updating_alfam_json = {'name': 'Alfam',
                                   'abouts': [about_en, about_ar, about_tr],
                                   'features': [context.swimming_pool.id, context.free_wifi.id],
                                   # 'cover': 'https://images.pexels.com/photos/97904/pexels-photo-97904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
                                   'geo_longitude': '35.15010', 'geo_latitude': '33.90111',
                                   'address': 'Next to Computer Department',
                                   'contact_name': 'Yaser', 'contact_email': 'yaser@gmail.com',
                                   'contact_number': '+908501531', 'contact_fax': '+801561561'}

    context.deserialized_data = ClientDormManagementSerializer(data=context.updating_alfam_json)
    print(context.deserialized_data.is_valid())
    print(context.deserialized_data.errors)


@then('validate the deserialized data for updating alfam')
def test(context):
    assert context.deserialized_data.is_valid() == True


@when('hitting PUT /manager-dorms/{alfam-id}')
def act(context):
    request = APIRequestFactory().put('', context.updating_alfam_json, format='json')
    force_authenticate(request, context.john)
    view = DormManagementViewSet.as_view(actions={'put': 'update'})
    context.response = view(request, pk=context.alfam.id)


@then('get 200 OK for updating alfam')
def test(context):
    # print(context.response.data)
    assert context.response.status_code == status.HTTP_200_OK
    assert str(Dormitory.objects.all()[0].about.data).count('Luxury Alfam') == 1
    assert str(Dormitory.objects.all()[0].about.data).count('الفام الفخيم') == 1
    assert str(Dormitory.objects.all()[0].about.data).count('Super Alfam') == 1


@when('hitting PUT /manager-dorms/{alfam-id}/cover with new image')
def act(context):
    uploaded_file = create_uploaded_file(context, 'alfam-photo.jpeg')
    cover_json = {'cover': uploaded_file}

    client = APIClient()
    client.force_authenticate(context.john)
    url = reverse('engine:manager-dorms-update-cover', kwargs={'pk': context.alfam.id})
    context.response = client.put(url, cover_json, format='multipart')


@then('get 201 CREATED for adding alfam cover')
def test(context):
    print(context.response.data)
    assert context.response.status_code == status.HTTP_200_OK
    assert Dormitory.objects.filter(name='Alfam').first().cover != None
    assert os.path.exists(context.expected_file_path) == True
    os.remove(context.expected_file_path)
