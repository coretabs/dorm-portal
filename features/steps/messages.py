from django.test import TestCase
from behave import *

from api.engine.models import Message

@when('making a message')
def setUp(self):
    self.message = Message(subject='Hello')

@then('check the message')
def test_model_can_create_a_message(self):
    print('qooq', self.message.subject)
    #self.assertEqual(1, 1)
    assert self.message.subject is 'Hello'