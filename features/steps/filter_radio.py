from behave import given, when, then

from api.engine.models import *

from features.steps.factory import *


@given('we have 1 dormitory with 2 rooms')
def arrange(context):

    category_public = create_category('public')
    context.alfam = create_dorm('Alfam', category_public)

    context.options = [RadioOption(name='Breakfast'),
                       RadioOption(name='Dinner'),
                       RadioOption(name='Both')]

    context.meals = create_radio_filter(context.options, 'Meals')

    context.meals_choice1 = create_radio_choice(context.options[0], context.meals)
    context.room1 = create_room_with_radio_choices(context.alfam, [context.meals_choice1, ])

    context.meals_choice2 = create_radio_choice(context.options[1], context.meals)
    context.room2 = create_room_with_radio_choices(context.alfam, [context.meals_choice2, ])
    context.room3 = create_room_with_radio_choices(context.alfam, [context.meals_choice2, ])

    context.room4 = create_room(context.alfam)


@when('filtering alfam rooms by meal Breakfast')
def act(context):
    choosen_option_id = [context.meals_choice1.selected_option.id, ]
    filters = [context.meals.get_query(choosen_option_id), ]
    context.filtered_dorm_alfam = Dormitory.objects.apply_room_filters(filters)


@then('get alfam dormitory with just one room having Breakfast')
def test(context):
    assert context.filtered_dorm_alfam.first().room_characteristics.all().count() == 1
    assert context.filtered_dorm_alfam.first()\
        .room_characteristics.first()\
        .radio_choices.first().selected_option.name == 'Breakfast'


@when('filtering alfam rooms by meal Dinner')
def act(context):
    choosen_option_id = [context.meals_choice2.selected_option.id, ]
    filters = [context.meals.get_query(choosen_option_id), ]
    context.filtered_dorm_alfam = Dormitory.objects.apply_room_filters(filters)


@then('get alfam dormitory with just two room having Dinner')
def test(context):
    assert context.filtered_dorm_alfam.first().room_characteristics.all().count() == 2

    assert context.filtered_dorm_alfam.first()\
        .room_characteristics.all()[0]\
        .radio_choices.first().selected_option.name == 'Dinner'

    assert context.filtered_dorm_alfam.first()\
        .room_characteristics.all()[1]\
        .radio_choices.first().selected_option.name == 'Dinner'


@when('filtering alfam rooms by meal Breakfast & Dinner')
def act(context):
    choosen_option_ids = [context.meals_choice1.selected_option.id,
                          context.meals_choice2.selected_option.id]
    filters = [context.meals.get_query(choosen_option_ids), ]
    context.filtered_dorm_alfam = Dormitory.objects.apply_room_filters(filters)


@then('get dormitory with all room having Breakfast & Dinner')
def test(context):
    assert context.filtered_dorm_alfam.first().room_characteristics.all().count() == 3

    assert context.filtered_dorm_alfam.first()\
        .room_characteristics.all()[0]\
        .radio_choices.first().selected_option.name == 'Breakfast'

    assert context.filtered_dorm_alfam.first()\
        .room_characteristics.all()[1]\
        .radio_choices.first().selected_option.name == 'Dinner'

    assert context.filtered_dorm_alfam.first()\
        .room_characteristics.all()[2]\
        .radio_choices.first().selected_option.name == 'Dinner'
