from django.test import TestCase
from behave import given, when, then

from features.steps.factory import *

from api.engine.models import Dormitory, RoomCharacteristics


@given('we have 2 dormitories (and 1 room each) with some quota')
def arrange(self):
    category_public = create_category('public')
    self.alfam = create_dorm('Alfam', category_public)

    self.room1 = create_room(self.alfam)
    self.room1.allowed_quota = 5
    self.room1.save()

    self.dovec = create_dorm('Dovec', category_public)

    self.room2 = create_room(self.dovec)
    self.room1.allowed_quota = 0
    self.room2.save()


@when('getting available dorms')
def act(self):
    self.filtered_dorm = Dormitory.objects.available()


@then('get alfam dormitory and not getting dovec')
def test(self):
    assert self.filtered_dorm.count() == 1
    assert self.filtered_dorm.first().name == 'Alfam'
