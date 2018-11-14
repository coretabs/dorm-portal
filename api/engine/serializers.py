from django.db import models as django_models

from rest_framework import serializers

from rest_polymorphic.serializers import PolymorphicSerializer

from .models import Filter, RadioFilter, IntegralFilter, FeatureFilter, Option


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


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = ('id', 'name')


class RadioFilterSerializer(serializers.ModelSerializer):

    is_checkbox = serializers.BooleanField(default=True)
    is_integral = serializers.BooleanField(default=False)
    options = OptionSerializer(many=True)

    class Meta:
        model = RadioFilter
        fields = ('id', 'name', 'is_checkbox', 'is_integral', 'options')


class AddtionalFiltersSerializer(PolymorphicSerializer):

    model_serializer_mapping = {
        IntegralFilter: IntegralFilterSerializer,
        RadioFilter: RadioFilterSerializer,
    }


class FeatureFiltersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureFilter
        fields = ('id', 'name')


class FiltersSerializer(serializers.Serializer):
    main_filters = serializers.SerializerMethodField()
    additional_filters = serializers.SerializerMethodField()
    dorm_features = serializers.SerializerMethodField()
    room_features = serializers.SerializerMethodField()

    def get_main_filters(self, obj):
        filters = Filter.objects.main_filters()
        return RadioFilterSerializer(filters, many=True).data

    def get_additional_filters(self, obj):
        filters = Filter.objects.additional_filters()
        return AddtionalFiltersSerializer(filters, many=True).data

    def get_dorm_features(self, obj):
        filters = Filter.objects.dorm_features()
        return FeatureFilterSerializer(filters, many=True).data

    def get_room_features(self, obj):
        filters = Filter.objects.room_features()
        return FeatureFilterSerializer(filters, many=True).data
