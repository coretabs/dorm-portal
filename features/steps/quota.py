from django.test import TestCase
from behave import given, when, then

from features.steps.factory import *

from api.engine.models import Dormitory, RoomCharacteristics


@given('we have 2 dormitories (and 1 room each) with some quota')
def arrange(context):
    category_public = create_category('public')
    context.alfam = create_dorm('Alfam', category_public)

    context.room1 = create_room(context.alfam)
    context.room1.allowed_quota = 5
    context.room1.save()

    context.dovec = create_dorm('Dovec', category_public)

    context.room2 = create_room(context.dovec)
    context.room1.allowed_quota = 0
    context.room2.save()


@when('getting available dorms')
def act(context):
    context.filtered_dorm = Dormitory.objects.available()


@then('get alfam dormitory and not getting dovec')
def test(context):
    assert context.filtered_dorm.count() == 1
    assert context.filtered_dorm.first().name == 'Alfam'
