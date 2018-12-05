from django.db import models as django_models

from rest_framework import serializers

from i18nfield.rest_framework import I18nField

from rest_polymorphic.serializers import PolymorphicSerializer

from api import settings

from . import models


class FeatureFilterSerializer(serializers.ModelSerializer):
    # name = I18nField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        model = models.FeatureFilter
        fields = ('id', 'name')


class IntegralFilterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_checkbox = serializers.BooleanField(default=False)
    is_integral = serializers.BooleanField(default=True)
    value = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.name)

    def get_value(self, obj):
        return obj.integralfilter.integral_choices.aggregate(
            django_models.Max('selected_number'), django_models.Min('selected_number'))

    class Meta:
        model = models.IntegralFilter
        fields = ('id', 'name', 'is_checkbox', 'is_integral', 'value')


class RadioOptionSerializer(serializers.ModelSerializer):
    # name = I18nField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        model = models.RadioOption
        fields = ('id', 'name')


class RadioFilterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_checkbox = serializers.BooleanField(default=True)
    is_integral = serializers.BooleanField(default=False)
    options = RadioOptionSerializer(many=True)

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        model = models.RadioFilter
        fields = ('id', 'name', 'is_checkbox', 'is_integral', 'options')


class AddtionalFiltersSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        models.IntegralFilter: IntegralFilterSerializer,
        models.RadioFilter: RadioFilterSerializer,
    }


class DormitoryCategorySerializer(serializers.ModelSerializer):
    # name = I18nField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        model = models.DormitoryCategory
        fields = ('id', 'name')


class ClientReturnedFiltersSerializer(serializers.Serializer):
    category_options = serializers.SerializerMethodField()
    duration_options = serializers.SerializerMethodField()
    additional_filters = serializers.SerializerMethodField()
    dorm_features = serializers.SerializerMethodField()
    room_features = serializers.SerializerMethodField()

    def get_category_options(self, obj):
        categories = models.DormitoryCategory.objects.all()
        return DormitoryCategorySerializer(categories, many=True).data

    def get_duration_options(self, obj):
        duration_filter = models.Filter.objects.filter(name__contains='Duration').first()
        return RadioOptionSerializer(duration_filter.options, many=True).data

    def get_additional_filters(self, obj):
        filters = models.Filter.objects.additional_filters()
        return AddtionalFiltersSerializer(filters, many=True).data

    def get_dorm_features(self, obj):
        filters = models.Filter.objects.dorm_features()
        return FeatureFilterSerializer(filters, many=True).data

    def get_room_features(self, obj):
        filters = models.Filter.objects.room_features()
        return FeatureFilterSerializer(filters, many=True).data


class ClientAddtionalFiltersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    choosen_options_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    min_value = serializers.IntegerField(required=False)
    max_value = serializers.IntegerField(required=False)

    class Meta:
        model = models.RadioFilter
        fields = ('id', 'choosen_options_ids', 'min_value', 'max_value')


class ClientFeaturesSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    class Meta:
        fields = ('id', )


class ClientAcceptedFiltersSerializer(serializers.Serializer):
    category_selected_option_id = serializers.IntegerField(required=False)
    duration_option_id = serializers.IntegerField(required=False)
    additional_filters = ClientAddtionalFiltersSerializer(many=True, required=False)
    dorm_features = ClientFeaturesSerializer(many=True, required=False)
    room_features = ClientFeaturesSerializer(many=True, required=False)


class RoomFeaturesSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        fields = ('name')


class RadioChoiceSerializer(serializers.ModelSerializer):
    filter_name = serializers.SerializerMethodField()
    choice = serializers.SerializerMethodField()

    def get_filter_name(self, obj):
        return str(obj.related_filter.name)

    def get_choice(self, obj):
        return str(obj.selected_option.name)

    class Meta:
        model = models.RadioChoice
        fields = ('filter_name', 'choice')


class IntegralChoiceSerializer(serializers.ModelSerializer):
    filter_name = serializers.SerializerMethodField()
    choice = serializers.SerializerMethodField()

    def get_filter_name(self, obj):
        return str(obj.related_filter.name)

    def get_choice(self, obj):
        return obj.selected_number

    class Meta:
        model = models.IntegralChoice
        fields = ('filter_name', 'choice')


class ChoiceSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        models.IntegralChoice: IntegralChoiceSerializer,
        models.RadioChoice: RadioChoiceSerializer,
    }


class PhotoSerializer(serializers.Serializer):
    url = serializers.ImageField()
    url = serializers.BooleanField(default=False)

    class Meta:
        fields = ('url', 'is_3d')


class RoomSerializer(serializers.ModelSerializer):
    rooms_left = serializers.IntegerField(source='allowed_quota')

    photos = PhotoSerializer(many=True)

    price = serializers.SerializerMethodField()
    room_type = serializers.SerializerMethodField()
    people_allowed_number = serializers.SerializerMethodField()

    choices = serializers.SerializerMethodField()
    features = RoomFeaturesSerializer(many=True)

    def get_price(self, obj):
        return obj.get_price()

    def get_room_type(self, obj):
        return obj.get_price()

    def get_people_allowed_number(self, obj):
        return obj.get_price()

    def get_choices(self, obj):
        #choices = obj.radio_choices.all() | obj.integral_choices.all()
        choices = models.Choice.objects.filter(django_models.Q(
            id__in=obj.radio_choices.all()) | django_models.Q(id__in=obj.integral_choices.all()))
        return ChoiceSerializer(choices, many=True).data

    class Meta:
        model = models.RoomCharacteristics
        fields = ('id', 'rooms_left',
                  'photos',
                  'price', 'room_type', 'people_allowed_number',
                  'choices', 'features')


class DormSerializer(serializers.ModelSerializer):
    features = FeatureFilterSerializer(many=True)
    room_characteristics = RoomSerializer(many=True)

    class Meta:
        model = models.Dormitory
        fields = ('id', 'name', 'features', 'room_characteristics')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = ('symbol', 'code',)


class LanguageSerailizer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()


class LocaleSerailizer(serializers.Serializer):
    currencies = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()

    def get_currencies(self, obj):
        currencies = models.Currency.objects.all()
        return CurrencySerializer(currencies, many=True).data

    def get_languages(self, obj):
        languages = [{'code': code, 'name': name} for code, name in settings.LANGUAGES]

        return LanguageSerailizer(languages, many=True).data
