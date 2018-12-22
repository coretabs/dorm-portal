from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework import status

from behave import given, when, then

from api.engine.models import *
from api.engine.serializers import *
from api.engine.views import *

from features.steps.factory import *


@given('we have 2 dormitory with 4 rooms with couple of choices')
def arrange(self):
    create_alfam_dovec_with_4_rooms(self)


@when('not doing any filtering for the dorms')
def act(self):
    self.filtered_dorms = Dormitory.objects.superfilter()


@then('get the 2 dorms with the 4 rooms')
def test(self):
    assert self.filtered_dorms.count() == 2
    assert self.filtered_dorms.all()[0].room_characteristics.count() == 2
    assert self.filtered_dorms.all()[1].room_characteristics.count() == 2


@then('get the rooms left equals the sum quota')
def test(self):
    assert self.filtered_dorms.count() == 2
    assert self.filtered_dorms.all()[0].rooms_left_in_dorm == 10
    assert self.filtered_dorms.all()[1].rooms_left_in_dorm == 10


@when('one of the alfam rooms has no quota')
def act(self):
    self.room1.allowed_quota = 0
    self.room1.save()
    self.filtered_dorms = Dormitory.objects.superfilter()


@then('get all the room except the one with no quota')
def test(self):
    assert self.filtered_dorms.count() == 2
    assert self.filtered_dorms.all()[0].room_characteristics.count() == 1
    assert self.filtered_dorms.all()[1].room_characteristics.count() == 2


@then('return the quota back for the alfam room')
def test(self):
    self.room1.allowed_quota = 5
    self.room1.save()


@when('filter free wifi')
def act(self):
    self.filtered_dorms = Dormitory.objects.superfilter(dorm_features_ids=[self.free_wifi.id, ])


@then('get only dovec which has free wifi with two rooms')
def test(self):
    assert self.filtered_dorms.count() == 1
    assert self.filtered_dorms.first().name == 'Dovec'
    assert self.filtered_dorms.all()[0].room_characteristics.count() == 2


@when('filter price between 1100 and 1800')
def act(self):
    price_choice = {'id': self.price_filter.id, 'min_value': 1100, 'max_value': 1800}
    self.filtered_dorms = Dormitory.objects.superfilter(radio_integeral_choices=[price_choice, ])


@then('get 2 dorms with 1 room for each (1200, 1700)')
def test(self):
    assert self.filtered_dorms.count() == 2
    assert self.filtered_dorms.all()[0].room_characteristics.count() == 1
    assert self.filtered_dorms.all()[1].room_characteristics.count() == 1


@when('filter PUBLIC dorm price between 1100 and 1800')
def act(self):
    price_choice = {'id': self.price_filter.id, 'min_value': 1100, 'max_value': 1800}
    self.filtered_dorms = Dormitory.objects.superfilter(category_id=self.category_public.id,
                                                        radio_integeral_choices=[price_choice, ])


@then('get alfam dorm with just 1 room (1200)')
def test(self):
    assert self.filtered_dorms.count() == 1
    assert self.filtered_dorms.first().name == 'Alfam'

    assert self.filtered_dorms.all()[0].room_characteristics.count() == 1
    assert self.filtered_dorms.all()[0].room_characteristics.first().price == 1200


@when('filter meals (breakfast & both) + luxury shower')
def act(self):
    breakfast_both = {'id': self.meals.id, 'choosen_options_ids': [
        self.meals_choice_breakfast.selected_option.id, self.meals_choice_both.selected_option.id]}

    self.filtered_dorms = Dormitory.objects.superfilter(
        radio_integeral_choices=[breakfast_both, ],
        room_features_ids=[self.luxury_shower.id, ])


@then('get only dovec with two rooms')
def test(self):
    assert self.filtered_dorms.count() == 1
    assert self.filtered_dorms.first().name == 'Dovec'
    assert self.filtered_dorms.all()[0].room_characteristics.count() == 2


@when('filter meals (without any option sent)')
def act(self):
    breakfast_both = {'id': self.meals.id, 'choosen_options_ids': []}

    self.filtered_dorms = Dormitory.objects.superfilter(
        radio_integeral_choices=[breakfast_both, ],)


@then('ignore the meals filter')
def test(self):
    assert self.filtered_dorms.count() == 2
    assert self.filtered_dorms.all()[0].room_characteristics.count() == 2
    assert self.filtered_dorms.all()[1].room_characteristics.count() == 2


@when('(breakfast&both) + luxuryshower + airconidtioner + price(1500,2000) + bathrooms(1,2)')
def act(self):
    price_choice = {'id': self.price_filter.id, 'min_value': 1500, 'max_value': 2000}
    bathroom_choice = {'id': self.bathrooms.id, 'min_value': 1, 'max_value': 2}

    breakfast_both = {'id': self.meals.id, 'choosen_options_ids': [
        self.meals_choice_breakfast.selected_option.id, self.meals_choice_both.selected_option.id]}

    self.filtered_dorms = Dormitory.objects.superfilter(
        radio_integeral_choices=[breakfast_both, price_choice, bathroom_choice],
        room_features_ids=[self.luxury_shower.id, self.air_conditioner.id])


@then('get only dovec with one room only')
def test(self):
    assert self.filtered_dorms.count() == 1
    assert self.filtered_dorms.first().name == 'Dovec'
    assert self.filtered_dorms.all()[0].room_characteristics.count() == 1


@when('deserialize the same filter above')
def act(self):
    price_choice = {'id': self.price_filter.id, 'min_value': 1500, 'max_value': 2000}
    bathroom_choice = {'id': self.bathrooms.id, 'min_value': 1, 'max_value': 2}
    breakfast_both = {'id': self.meals.id, 'choosen_options_ids': [
        self.meals_choice_breakfast.selected_option.id, self.meals_choice_both.selected_option.id]}

    self.same_filter_above_json = {'additional_filters': [price_choice, bathroom_choice, breakfast_both],
                                   'room_features': [self.luxury_shower.id, self.air_conditioner.id]}

    self.deserialized_data = ClientAcceptedFiltersSerializer(data=self.same_filter_above_json)


@then('validate the deserialized filters successfully')
def test(self):
    assert self.deserialized_data.is_valid() == True


@when('serialize the returned dorms data from the last filters')
def act(self):
    self.serialized_dorms = DormSerializer(self.filtered_dorms, many=True)
    self.serialized_dorms_string = str(self.serialized_dorms.data)


@then('get deserialize data for (only dovec with one room only)')
def test(self):
    print(self.serialized_dorms_string)
    assert self.serialized_dorms_string.count("('name', 'Dovec')") == 1


@when('hitting POST /dorms endpoint with filter above')
def act(self):
    request = APIRequestFactory().post(reverse('engine:dorms-list'),
                                       self.same_filter_above_json, format='json')
    view = DormViewSet.as_view(actions={'post': 'create'})
    self.response = view(request)


@then('get 200 OK with data for (only dovec with one room only)')
def test(self):
    assert self.response.status_code == status.HTTP_200_OK

    returned_dorms = self.response.render().data[0]

    number_of_returned_json_filters = len(list(returned_dorms))
    assert number_of_returned_json_filters == 9

    print(self.response.render().data)
    assert str(self.response.render().data).count("('name', 'Dovec')") == 1
