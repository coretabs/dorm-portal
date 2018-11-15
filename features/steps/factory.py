from api.engine.models import *


def create_category(name):
    DormitoryCategory(name='public').save()
    result = DormitoryCategory.objects.filter(name=name).first()

    return result


def create_dorm(name, category):
    result = Dormitory(name=name)
    result.category = category
    result.save()

    return result


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


def create_room_with_radio_integral_features(dorm, radio_choices, integral_choices, features):
    result = RoomCharacteristics(dormitory=dorm)
    result.save()

    for choice in radio_choices:
        result.radio_choices.add(choice)
    result.save()

    for choice in integral_choices:
        result.integral_choices.add(choice)
    result.save()

    for feature in features:
        result.features.add(feature)
    result.save()

    return result


def create_alfam_dovec_with_4_rooms():

    category_public = create_category('public')
    category_private = create_category('private')

    alfam = create_dorm('Alfam', category_public)
    dovec = create_dorm('Dovec', category_private)

    swimming_pool = create_dorm_feature('Swimming pool')
    free_wifi = create_dorm_feature('Free WiFi')

    alfam.features.add(swimming_pool)
    alfam.save()
    dovec.features.add(free_wifi)
    dovec.save()

    luxury_shower = create_room_feature('Luxury shower')
    air_conditioner = create_room_feature('Air Conditioner')

    integral_filter = IntegralFilter(name='price')
    integral_filter.save()
    price_1000 = create_integral_choice(integral_filter, 1000)
    price_1200 = create_integral_choice(integral_filter, 1200)
    price_1700 = create_integral_choice(integral_filter, 1700)
    price_2000 = create_integral_choice(integral_filter, 2000)

    bathrooms = IntegralFilter(name='bathroom')
    bathrooms.save()
    bathrooms1 = create_integral_choice(bathrooms, 1)
    bathrooms2 = create_integral_choice(bathrooms, 2)

    meal_options = [Option(name='Breakfast'), Option(name='Dinner'), Option(name='Both')]
    meals = create_radio_filter(meal_options, 'meals')
    meals_choice_breakfast = create_radio_choice(meal_options[0], meals)
    meals_choice_dinner = create_radio_choice(meal_options[1], meals)

    options_academic_year = [Option(name='Spring'), Option(name='Winter'),
                             Option(name='Summer'), Option(name='Full year')]
    academic_year = create_radio_filter(options_academic_year, 'academic year')
    academic_year_choice_spring = create_radio_choice(options_academic_year[0], academic_year)
    academic_year_choice_winter = create_radio_choice(options_academic_year[1], academic_year)
    academic_year_choice_summer = create_radio_choice(options_academic_year[2], academic_year)
    academic_year_choice_full = create_radio_choice(options_academic_year[3], academic_year)

    room1 = create_room_with_radio_integral_features(
        alfam,
        [academic_year_choice_spring, ],
        [price_1000, ],
        [air_conditioner, ])

    room2 = create_room_with_radio_integral_features(
        alfam,
        [academic_year_choice_spring, meals_choice_breakfast],
        [price_2000, ],
        [luxury_shower, air_conditioner])

    room3 = create_room_with_radio_integral_features(
        dovec,
        [academic_year_choice_spring, meals_choice_breakfast],
        [price_2000, ],
        [luxury_shower, air_conditioner])

    room4 = create_room_with_radio_integral_features(
        dovec,
        [academic_year_choice_spring, meals_choice_breakfast],
        [price_2000, ],
        [luxury_shower, air_conditioner])

    return alfam, dovec
