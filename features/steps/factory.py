from api.engine.models import *


def create_category(name):
    DormitoryCategory(name=name).save()
    result = DormitoryCategory.objects.filter(name=name).first()

    return result


def create_dorm(name, category):
    result = Dormitory(name=name)
    result.category = category
    result.save()

    return result


def create_integral_choice(integral_filter, number):
    result = IntegralChoice(selected_number=number)
    result.related_filter = integral_filter
    result.save()

    result = IntegralChoice.objects.filter(selected_number=number).first()

    return result


def create_radio_filter(options, name):
    result = RadioFilter(name=name)
    result.save()

    for option in options:
        option.related_filter = result
        option.save()
        option = RadioOption.objects.filter(name=option.name)

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
    result.related_filter = radio_filter
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
    result = RoomCharacteristics(dormitory=dorm, allowed_quota=1)
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


def create_alfam_dovec_with_4_rooms(self):

    self.category_public = create_category('public')
    self.category_private = create_category('private')

    self.alfam = create_dorm('Alfam', self.category_public)
    self.dovec = create_dorm('Dovec', self.category_private)

    self.swimming_pool = create_dorm_feature('Swimming pool')
    self.free_wifi = create_dorm_feature('Free WiFi')

    self.alfam.features.add(self.swimming_pool)
    self.alfam.save()
    self.dovec.features.add(self.free_wifi)
    self.dovec.save()

    self.luxury_shower = create_room_feature('Luxury shower')
    self.air_conditioner = create_room_feature('Air Conditioner')

    self.price_filter = IntegralFilter(name='price')
    self.price_filter.save()
    self.price_1000 = create_integral_choice(self.price_filter, 1000)
    self.price_1200 = create_integral_choice(self.price_filter, 1200)
    self.price_1700 = create_integral_choice(self.price_filter, 1700)
    self.price_2000 = create_integral_choice(self.price_filter, 2000)

    self.bathrooms = IntegralFilter(name='bathroom')
    self.bathrooms.save()
    self.bathrooms1 = create_integral_choice(self.bathrooms, 1)
    self.bathrooms2 = create_integral_choice(self.bathrooms, 2)

    self.meal_options = [RadioOption(name='Breakfast'),
                         RadioOption(name='Dinner'),
                         RadioOption(name='Both')]
    self.meals = create_radio_filter(self.meal_options, 'meals')
    self.meals_choice_breakfast = create_radio_choice(self.meal_options[0], self.meals)
    self.meals_choice_dinner = create_radio_choice(self.meal_options[1], self.meals)
    self.meals_choice_both = create_radio_choice(self.meal_options[2], self.meals)

    self.options_academic_year = [RadioOption(name='Spring'), RadioOption(name='Winter'),
                                  RadioOption(name='Summer'), RadioOption(name='Full year')]
    self.academic_year = create_radio_filter(self.options_academic_year, 'academic year')
    self.academic_year_choice_spring = create_radio_choice(
        self.options_academic_year[0], self.academic_year)
    self.academic_year_choice_winter = create_radio_choice(
        self.options_academic_year[1], self.academic_year)
    self.academic_year_choice_summer = create_radio_choice(
        self.options_academic_year[2], self.academic_year)
    self.academic_year_choice_full = create_radio_choice(
        self.options_academic_year[3], self.academic_year)

    self.room1 = create_room_with_radio_integral_features(
        self.alfam,
        [self.academic_year_choice_spring, ],
        [self.price_1000, ],
        [])

    self.room2 = create_room_with_radio_integral_features(
        self.alfam,
        [self.meals_choice_breakfast, self.academic_year_choice_spring],
        [self.price_1200, self.bathrooms1],
        [self.air_conditioner, ])

    self.room3 = create_room_with_radio_integral_features(
        self.dovec,
        [self.meals_choice_breakfast, self.academic_year_choice_spring],
        [self.price_1700, ],
        [self.luxury_shower, ])

    self.room4 = create_room_with_radio_integral_features(
        self.dovec,
        [self.meals_choice_both, self.academic_year_choice_full],
        [self.price_2000, self.bathrooms2],
        [self.luxury_shower, self.air_conditioner])
