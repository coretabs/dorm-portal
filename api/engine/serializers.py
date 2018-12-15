from django.db import models as django_models
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import serializers

from allauth.account.forms import ResetPasswordForm, default_token_generator, UserTokenForm
from allauth.account.adapter import get_adapter
from allauth.account.utils import send_email_confirmation, user_pk_to_url_str, setup_user_email
from allauth.account import app_settings as allauth_settings


from allauth.utils import email_address_exists

from i18nfield.rest_framework import I18nField

from rest_polymorphic.serializers import PolymorphicSerializer

from api import settings

from . import models


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')
    is_manager = serializers.BooleanField(read_only=True)
    class Meta:
        model = models.User
        fields = ('name', 'is_manager',)
                  #'current_step', 'reservation_id')

class ReceiptSerializer(serializers.ModelSerializer):
    url = serializers.URLField()
    class Meta:
        model = models.ReceiptPhoto
        fields = ('url', 'upload_receipt_date')

class ReservationRoomCharacteristicsSerializer(serializers.ModelSerializer):
    room_type = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    def get_room_type(self, obj):
        return str(obj.room_type)

    def get_duration(self, obj):
        return str(obj.duration)

    class Meta:
        model = models.RoomCharacteristics
        fields = ('id', 'price', 'price_currency',
                  'room_type', 'duration', 'people_allowed_number')


class ClientReservationManagementSerializer(serializers.ModelSerializer):
    confirmation_deadline_date = serializers.DateField(required=False)
    status = serializers.IntegerField(required=False)
    follow_up_message = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        status = validated_data.get('status', None)
        if status:
            if str(status) not in [status[0] for status in models.Reservation.STATUS_CHOICES]:
                raise serializers.ValidationError("Status doesn't exist!") 

            validated_data['status'] = str(status)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

    class Meta:
        model = models.Reservation
        fields = ('confirmation_deadline_date', 'status', 'follow_up_message')

class ReservationManagementDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    room_characteristics = ReservationRoomCharacteristicsSerializer()
    receipts = ReceiptSerializer(many=True)
    
    class Meta:
        model = models.Reservation
        fields = ('id', 
                  'reservation_creation_date', 'confirmation_deadline_date', 'status',
                  'user', 'room_characteristics', 'receipts')


class ReservationManagementSerializer(serializers.Serializer):
    reservations = ReservationManagementDetailsSerializer(many=True)

    class Meta:
        fields = ('pending_reservations', 'rejected_reservations', 
                  'confirmed_reservations', 'waiting_for_manager_action_reservations', 
                  'manager_updated_reservations', 'expired_reservations',
                  'reservations')


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    "A user is already registered with this e-mail address.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user


class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if not email_address_exists(email):
            raise serializers.ValidationError('The e-mail address is not assigned '
                                              'to any user account')
        return email

    def save(self, *args, **kwargs):
        request = self.context.get('request')

        current_site = get_current_site(request)
        email = self.validated_data['email']

        user = models.User.objects.get(email__iexact=email)

        token_generator = kwargs.get(
            'token_generator', default_token_generator)
        temp_key = token_generator.make_token(user)

        path = f'/reset-password/{user_pk_to_url_str(user)}/{temp_key}'
        url = settings.BASE_URL + path
        context = {'current_site': current_site,
                   'user': user,
                   'password_reset_url': url,
                   'request': request}

        get_adapter().send_mail(
            'account/email/password_reset_key',
            email,
            context)

        return email

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    key = serializers.CharField()

    def validate_new_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, attrs):
        self.user_token_form = UserTokenForm(
            data={'uidb36': attrs['uid'], 'key': attrs['key']})

        if not self.user_token_form.is_valid():
            raise serializers.ValidationError('Invalid token')

        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError(
                'The two password fields did not match.')

        self.password = attrs['new_password1']

        return attrs

    def save(self):
        user = self.user_token_form.reset_user
        get_adapter().set_password(user, self.password)
        return user



class ResendConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password_reset_form_class = ResetPasswordForm

    def validate(self, attrs):
        self.reset_form = self.password_reset_form_class(
            data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return attrs

    def save(self):
        request = self.context.get('request')
        email = self.reset_form.cleaned_data['email']
        user = models.User.objects.get(email__iexact=email)
        send_email_confirmation(request, user, True)
        return email


class FeatureFilterSerializer(serializers.ModelSerializer):
    # name = I18nField()
    name = serializers.SerializerMethodField()
    icon = serializers.CharField(default='fa-check')

    def get_name(self, obj):
        return str(obj.name)

    class Meta:
        model = models.FeatureFilter
        fields = ('id', 'name', 'icon')


class IntegralFilterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_checkbox = serializers.BooleanField(default=False)
    is_integral = serializers.BooleanField(default=True)
    value = serializers.SerializerMethodField()
    min_value = serializers.SerializerMethodField()
    max_value = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.name)

    def get_value(self, obj):
        result = obj.integralfilter.integral_choices.aggregate(
            django_models.Max('selected_number'), django_models.Min('selected_number'))

        self.min_value = result['selected_number__min']
        self.max_value = result['selected_number__max']

        return [self.min_value, self.max_value]

    def get_min_value(self, obj):
        return self.min_value

    def get_max_value(self, obj):
        return self.max_value

    class Meta:
        model = models.IntegralFilter
        fields = ('id', 'name', 'is_checkbox', 'is_integral', 'value', 'min_value', 'max_value')


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
    url = serializers.URLField()
    is_3d = serializers.BooleanField(default=False)

    class Meta:
        fields = ('url', 'is_3d')


class ClientPhotoDormSerializer(serializers.Serializer):
    uploaded_photo = serializers.ImageField(required=False)
    url = serializers.URLField(required=False)
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

    room_type = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    choices = serializers.SerializerMethodField()
    features = RoomFeaturesSerializer(many=True)

    def get_room_type(self, obj):
        return str(obj.room_type)

    def get_duration(self, obj):
        return str(obj.duration)

    def get_choices(self, obj):
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
            instance.cover = cover
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
    about = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    room_characteristics = RoomSerializer(many=True)

    def get_main_info(self, obj):
        return DormSerializer(obj).data

    def get_about(self, obj):
        return str(obj.about)

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
