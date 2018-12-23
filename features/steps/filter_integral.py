from behave import given, when, then

from api.engine.models import *

from features.steps.factory import *


@given('we have 4 rooms different prices (alfam: 3 rooms, dovec: 1 room)')
def arrange(context):
    category_public = create_category('public')
    context.alfam = create_dorm('Alfam', category_public)

    context.price_filter = IntegralFilter(name='Price')
    context.price_filter.save()

    context.price_alfam1 = create_integral_choice(context.price_filter, 1000)
    context.price_alfam2 = create_integral_choice(context.price_filter, 1200)
    context.price_alfam3 = create_integral_choice(context.price_filter, 1700)

    context.room1 = create_room_with_integral_choices(context.alfam, [context.price_alfam1, ])
    context.room2 = create_room_with_integral_choices(context.alfam, [context.price_alfam2, ])
    context.room3 = create_room_with_integral_choices(context.alfam, [context.price_alfam3, ])

    context.dovec = create_dorm('Dovec', category_public)

    context.price_dovec1 = create_integral_choice(context.price_filter, 2000)
    context.room4 = create_room_with_integral_choices(context.dovec, [context.price_dovec1, ])


@when('filtering alfam prices between 500, 1500')
def act(context):
    filters = [context.price_filter.get_query(500, 1500), ]
    context.filtered_dorm_alfam = Dormitory.objects.filter(
        name='Alfam').apply_room_filters(filters)


@then('get alfam dormitory with just 2 rooms')
def test(context):
    assert context.filtered_dorm_alfam.first().name == 'Alfam'
    assert context.filtered_dorm_alfam.first().room_characteristics.count() == 2


@when('filtering dovec with wrong price range')
def act(context):
    filters = [context.price_filter.get_query(500, 1500), ]
    context.filtered_dorm_dovec = Dormitory.objects.filter(
        name='Dovec').apply_room_filters(filters)


@then('not getting any dorm in dovec for wrong price')
def test(context):
    assert context.filtered_dorm_dovec.count() == 0
