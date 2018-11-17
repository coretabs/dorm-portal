from django.db import models as django_models

from rest_framework import serializers

from rest_polymorphic.serializers import PolymorphicSerializer

from .models import (Filter, RadioFilter, IntegralFilter, FeatureFilter, RadioOption,
                     DormitoryCategory, Dormitory, RoomCharacteristics)


class FeatureFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureFilter
        fields = ('id', 'name')


class IntegralFilterSerializer(serializers.ModelSerializer):
    is_checkbox = serializers.BooleanField(default=False)
    is_integral = serializers.BooleanField(default=True)
    value = serializers.SerializerMethodField()

    def get_value(self, obj):
        return obj.integralfilter.integral_choices.aggregate(
            django_models.Max('selected_number'), django_models.Min('selected_number'))

    class Meta:
        model = IntegralFilter
        fields = ('id', 'name', 'is_checkbox', 'is_integral', 'value')


class RadioOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioOption
        fields = ('id', 'name')


class RadioFilterSerializer(serializers.ModelSerializer):
    is_checkbox = serializers.BooleanField(default=True)
    is_integral = serializers.BooleanField(default=False)
    options = RadioOptionSerializer(many=True)

    class Meta:
        model = RadioFilter
        fields = ('id', 'name', 'is_checkbox', 'is_integral', 'options')


class AddtionalFiltersSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        IntegralFilter: IntegralFilterSerializer,
        RadioFilter: RadioFilterSerializer,
    }


class DormitoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DormitoryCategory
        fields = ('id', 'name')


class ClientReturnedFiltersSerializer(serializers.Serializer):
    category_options = serializers.SerializerMethodField()
    academic_year_options = serializers.SerializerMethodField()
    additional_filters = serializers.SerializerMethodField()
    dorm_features = serializers.SerializerMethodField()
    room_features = serializers.SerializerMethodField()

    def get_category_options(self, obj):
        categories = DormitoryCategory.objects.all()
        return RadioOptionSerializer(categories, many=True).data

    def get_academic_year_options(self, obj):
        academic_year_filter = Filter.objects.filter(name='academic year').first()
        return RadioOptionSerializer(academic_year_filter.options, many=True).data

    def get_additional_filters(self, obj):
        filters = Filter.objects.additional_filters()
        return AddtionalFiltersSerializer(filters, many=True).data

    def get_dorm_features(self, obj):
        filters = Filter.objects.dorm_features()
        return FeatureFilterSerializer(filters, many=True).data

    def get_room_features(self, obj):
        filters = Filter.objects.room_features()
        return FeatureFilterSerializer(filters, many=True).data


class ClientAddtionalFiltersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    choosen_options_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    min_value = serializers.IntegerField(required=False)
    max_value = serializers.IntegerField(required=False)

    class Meta:
        model = RadioFilter
        fields = ('id', 'choosen_options_ids', 'min_value', 'max_value')


class ClientFeaturesSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    class Meta:
        fields = ('id',)


class ClientAcceptedFiltersSerializer(serializers.Serializer):
    category_selected_option_id = serializers.IntegerField(required=False)
    academic_year_option_id = serializers.IntegerField(required=False)
    additional_filters = ClientAddtionalFiltersSerializer(many=True, required=False)
    dorm_features = ClientFeaturesSerializer(many=True, required=False)
    room_features = ClientFeaturesSerializer(many=True, required=False)


class RoomSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return obj.get_price()

    class Meta:
        model = RoomCharacteristics
        fields = ('id', 'price')


class DormSerializer(serializers.ModelSerializer):
    features = FeatureFilterSerializer(many=True)
    room_characteristics = RoomSerializer(many=True)

    class Meta:
        model = Dormitory
        fields = ('id', 'name', 'features', 'room_characteristics')
