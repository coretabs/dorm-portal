from behave import given, when, then

from api.engine.models import *

from features.steps.factory import *


@given('we have 2 dormitory with different features')
def arrange(context):

    context.swimming_pool = create_dorm_feature('Swimming pool')
    context.free_wifi = create_dorm_feature('Free WiFi')

    category_public = create_category('public')
    context.alfam = create_dorm('Alfam', category_public)

    context.alfam.features.add(context.swimming_pool)
    context.alfam.save()

    context.dovec = create_dorm('Dovec', category_public)

    context.dovec.features.add(context.free_wifi)
    context.dovec.save()


@when('filtering dorms by swimming pool')
def act(context):
    filters = [context.swimming_pool.get_query(), ]
    context.filtered_dorm_alfam = Dormitory.objects.apply_dorm_filters(filters)


@then('get only the dorm which has swimming pool')
def test(context):
    assert context.filtered_dorm_alfam.first().name == 'Alfam'
    assert context.filtered_dorm_alfam.all().count() == 1


@given('we have 2 dormitoroes with room-specific features')
def arrange(context):

    context.luxury_shower = create_room_feature('Luxury shower')
    context.air_conditioner = create_room_feature('Air Conditioner')

    context.room1 = create_room_with_features(
        context.alfam, [context.luxury_shower, context.air_conditioner])
    context.room2 = create_room_with_features(context.alfam, [context.air_conditioner, ])

    context.room3 = create_room(context.dovec)


@when('filtering dorms by having one room with luxury shower')
def act(context):
    filters = [context.luxury_shower.get_query(), ]
    context.filtered_dorms = Dormitory.objects.apply_room_filters(filters)


@then('get only alfam with just one room which has luxury shower')
def test(context):
    assert context.filtered_dorms.first().name == 'Alfam'
    assert context.filtered_dorms.count() == 1

    assert context.filtered_dorms.first().room_characteristics.count() == 1
    assert context.filtered_dorms.first().room_characteristics.first(
    ).features.first().name == 'Luxury shower'


@when('filtering dorms by luxury shower & air conditioner')
def act(context):
    filters = [context.luxury_shower.get_query(
    ), context.air_conditioner.get_query(), ]
    context.filtered_dorms = Dormitory.objects.apply_room_filters(filters)


@then('get only alfam with just one rooms having luxury shower & air conditioner')
def test(context):
    assert context.filtered_dorms.first().name == 'Alfam'
    assert context.filtered_dorms.count() == 1

    assert context.filtered_dorms.first().room_characteristics.all().count() == 1
    assert context.filtered_dorms.first().room_characteristics.first().features.all()[
        0].name == 'Luxury shower'
    assert context.filtered_dorms.first().room_characteristics.first().features.all()[
        1].name == 'Air Conditioner'


@when('filtering dorms by air conditioner')
def act(context):
    filters = [context.air_conditioner.get_query(), ]
    context.filtered_dorms = Dormitory.objects.apply_room_filters(filters)


@then('get only alfam with two rooms having air conditioner')
def test(context):
    assert context.filtered_dorms.first().name == 'Alfam'
    assert context.filtered_dorms.count() == 1

    assert context.filtered_dorms.first().room_characteristics.all().count() == 2
    # use exists
    assert context.filtered_dorms.first().room_characteristics.all(
    )[0].features.filter(name='Air Conditioner').count() == 1
    assert context.filtered_dorms.first().room_characteristics.all(
    )[1].features.filter(name='Air Conditioner').count() == 1
