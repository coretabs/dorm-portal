from django.test import TestCase
from behave import given, when, then

from api.engine.models import Dormitory, RoomCharacteristics

@given('we have 2 dormitories with some quota')
def prepare_dormitory(self):
    self.alfam = Dormitory(name='Alfam')
    self.alfam.save()

    self.room1 = RoomCharacteristics(dormitory=self.alfam, allowed_quota=5)
    self.room1.save()

    self.dovec = Dormitory(name='Dovec')
    self.dovec.save()

    self.room2 = RoomCharacteristics(dormitory=self.dovec, allowed_quota=0)
    self.room2.save()


@when('getting available dorms')
def filtering(self):
    self.filtered_dorm = Dormitory.objects.available()

@then('get alfam dormitory and not getting dovec')
def test_model_can_create_a_message(self):
    assert self.filtered_dorm.count() == 1
    assert self.filtered_dorm.first().name == 'Alfam'