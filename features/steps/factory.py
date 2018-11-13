from api.engine.models import *


def create_integral_filter(integral_choice, number):
    result = IntegralFilter(selected_number=number)
    result.integral_choice = integral_choice
    result.save()

    result = IntegralFilter.objects.filter(selected_number=number).first()

    return result


def create_radio_choice(options, name):
    result = RadioChoice(name=name)
    result.save()

    for option in options:
        option.radio_choice = result
        option.save()
        option = Option.objects.filter(name=option.name)

    result = RadioChoice.objects.filter(name=name).first()

    return result


def create_dorm_feature(name):
    result = FeatureChoice(name=name, is_dorm_feature=True)
    result.save()
    result = FeatureChoice.objects.filter(name=name).first()

    return result


def create_room_feature(name):
    result = FeatureChoice(name=name)
    result.save()
    result = FeatureChoice.objects.filter(name=name).first()

    return result


def create_radio_filter(selected_option, radio_choice):
    result = RadioFilter()
    result.selected_option = selected_option
    result.radio_choice = radio_choice
    result.save()

    result = RadioFilter.objects.get(pk=result.id)

    return result


def create_room_with_filters(dorm, filters):
    result = RoomCharacteristics(dormitory=dorm)
    result.save()

    for filter in filters:
        result.filters.add(filter)
    result.save()

    return result


def create_room_with_features(dorm, features):
    result = RoomCharacteristics(dormitory=dorm)
    result.save()

    for feature in features:
        result.features.add(feature)
    result.save()

    return result
