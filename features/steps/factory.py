from api.engine.models import *


def create_integral_choice(integral_filter, number):
    result = IntegralChoice(selected_number=number)
    result.integral_filter = integral_filter
    result.save()

    result = IntegralChoice.objects.filter(selected_number=number).first()

    return result


def create_radio_filter(options, name):
    result = RadioFilter(name=name)
    result.save()

    for option in options:
        option.radio_filter = result
        option.save()
        option = Option.objects.filter(name=option.name)

    result = RadioFilter.objects.filter(name=name).first()

    return result


def create_dorm_feature(name):
    result = FeatureFilter(name=name, is_dorm_feature=True)
    result.save()
    result = FeatureFilter.objects.filter(name=name).first()

    return result


def create_room_feature(name):
    result = FeatureFilter(name=name)
    result.save()
    result = FeatureFilter.objects.filter(name=name).first()

    return result


def create_radio_choice(selected_option, radio_filter):
    result = RadioChoice()
    result.selected_option = selected_option
    result.radio_filter = radio_filter
    result.save()

    result = RadioChoice.objects.get(pk=result.id)

    return result


def create_room_with_radio_choices(dorm, choices):
    result = RoomCharacteristics(dormitory=dorm)
    result.save()

    for choice in choices:
        result.radio_choices.add(choice)
    result.save()

    return result


def create_room_with_integral_choices(dorm, choices):
    result = RoomCharacteristics(dormitory=dorm)
    result.save()

    for choice in choices:
        result.integral_choices.add(choice)
    result.save()

    return result


def create_room_with_features(dorm, features):
    result = RoomCharacteristics(dormitory=dorm)
    result.save()

    for feature in features:
        result.features.add(feature)
    result.save()

    return result
