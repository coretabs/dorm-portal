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
    url = serializers.SerializerMethodField()
    is_3d = serializers.BooleanField(default=False)

    def get_url(self, obj):
        return generate_url(obj)

    class Meta:
        fields = ('url', 'is_3d')


class ClientPhotoDormSerializer(serializers.Serializer):
    uploaded_photo = serializers.ImageField(required=False)
    url = serializers.CharField(required=False)
    is_3d = serializers.BooleanField(default=False)

    def create(self, validated_data):
        dormitory = models.Dormitory.objects.get(pk=self.context.get('view').kwargs.get('dorm_pk'))
        uploaded_photo = validated_data.get('uploaded_photo', None)
        url = validated_data.get('url', None)

        if not url and not uploaded_photo:
            raise serializers.ValidationError('please add either url or uploaded_photo')

        if url:
            if not validated_data['is_3d']:
                raise serializers.ValidationError('url only for is_3d')
            instance = models.DormitoryPhoto(photo=url, is_3d=True, dormitory=dormitory)

        else:
            instance = models.DormitoryPhoto(photo=uploaded_photo, dormitory=dormitory)

        instance.save()

        return instance

    class Meta:
        fields = ('uploaded_photo', 'url', 'is_3d')


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
        return obj.get_room_type()

    def get_people_allowed_number(self, obj):
        return obj.get_people_allowed_number()

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


class ClientBankAccountSerializer(serializers.Serializer):
    bank_name = serializers.CharField(required=False)
    account_name = serializers.CharField(required=False)
    account_number = serializers.CharField(required=False)
    swift = serializers.CharField(required=False)
    iban = serializers.CharField(required=False)
    currency_code = serializers.CharField(required=False)

    def create(self, validated_data):
        dormitory = models.Dormitory.objects.get(pk=self.context.get('view').kwargs.get('dorm_pk'))
        currency = models.Currency.objects.get(code=validated_data['currency_code'])

        validated_data.pop('currency_code', None)
        validated_data['dormitory'] = dormitory
        validated_data['currency'] = currency

        instance = models.BankAccount(**validated_data)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    class Meta:
        fields = ('bank_name', 'account_name',
                  'account_number', 'swift', 'iban', 'currency_code')


class ClientDormManagementSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    abouts = serializers.ListField(child=I18nField(), required=False)
    features = ClientFeaturesSerializer(many=True, required=False)
    cover = serializers.ImageField(required=False)
    geo_longitude = serializers.CharField(required=False)
    geo_latitude = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    contact_name = serializers.CharField(required=False)
    contact_email = serializers.CharField(required=False)
    contact_number = serializers.CharField(required=False)
    contact_fax = serializers.CharField(required=False)

    def update(self, instance, validated_data):

        cover = validated_data.get('cover', None)
        if cover:
            pass
            validated_data.pop('cover', None)

        features = validated_data.get('features', None)
        if features:
            instance.features.clear()
            for serialized_feature in features:
                feature = models.FeatureFilter.objects.get(pk=serialized_feature['id'])
                instance.features.add(feature)
            validated_data.pop('features', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    class Meta:
        model = models.Dormitory
        fields = ('name', 'abouts', 'features',
                  'cover', 'photos',
                  'geo_longitude', 'geo_latitude', 'address',
                  'contact_name', 'contact_email', 'contact_number', 'contact_fax')


class DormManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dormitory
        fields = ('id', 'name', 'cover')


class BankAccountSerializer(serializers.ModelSerializer):
    currency_code = serializers.SerializerMethodField()

    def get_currency_code(self, obj):
        return obj.currency.code

    class Meta:
        model = models.BankAccount
        fields = ('id', 'bank_name', 'account_name',
                  'account_number', 'swift', 'iban', 'currency_code')


class DormManagementDetailsSerializer(serializers.ModelSerializer):
    bank_accounts = BankAccountSerializer(many=True)
    features = FeatureFilterSerializer(many=True)
    photos = PhotoSerializer(many=True)
    abouts = serializers.SerializerMethodField()

    def get_abouts(self, obj):
        return obj.about.data

    class Meta:
        model = models.Dormitory
        fields = ('name', 'abouts', 'bank_accounts', 'features',
                  'cover', 'photos',
                  'geo_longitude', 'geo_latitude', 'address',
                  'contact_name', 'contact_email', 'contact_number', 'contact_fax')


class DormSerializer(serializers.ModelSerializer):
    features = FeatureFilterSerializer(many=True)
    room_characteristics = RoomSerializer(many=True)
    rooms_left_in_dorm = serializers.IntegerField()

    class Meta:
        model = models.Dormitory
        fields = ('id', 'name', 'cover',
                  #'stars', 'number_of_reviews',
                  'geo_longitude', 'geo_latitude', 'address',
                  'rooms_left_in_dorm',
                  'features', 'room_characteristics')


class DormDetailsSerializer(serializers.ModelSerializer):
    main_info = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True)
    features = serializers.SerializerMethodField()
    room_characteristics = RoomSerializer(many=True)

    def get_main_info(self, obj):
        return DormSerializer(obj).data

    def get_features(self, obj):
        filters = models.Filter.objects.dorm_features()
        return FeatureFilterSerializer(filters, many=True).data

    class Meta:
        model = models.Dormitory
        fields = ('main_info',
                  'photos',
                  'about', 'contact_name', 'contact_email', 'contact_number', 'contact_fax',
                  'features',
                  #'number_of_reviews', 'reviews_average', 'reviews',
                  'room_characteristics')


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
