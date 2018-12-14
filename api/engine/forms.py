from django import forms

from i18nfield import forms as i18nforms

from api.engine import models


class FeatureFilterForm(forms.ModelForm):
    class Meta:
        name = models.FeatureFilter
        fields = ['name', 'is_dorm_feature']
        widgets = {
            'name': i18nforms.I18nTextInput,
        }


class IntegralFilterForm(forms.ModelForm):
    class Meta:
        name = models.IntegralFilter
        fields = ['name', 'is_optional']
        widgets = {
            'name': i18nforms.I18nTextInput,
        }


class RadioFilterForm(forms.ModelForm):
    class Meta:
        name = models.RadioFilter
        fields = ['name', 'is_optional']
        widgets = {
            'name': i18nforms.I18nTextInput,
        }


class RadioOptionForm(forms.ModelForm):
    class Meta:
        name = models.RadioOption
        fields = ['name', 'related_filter']
        widgets = {
            'name': i18nforms.I18nTextInput,
        }


class DormitoryCategoryForm(forms.ModelForm):
    class Meta:
        name = models.DormitoryCategory
        fields = ['name', ]
        widgets = {
            'name': i18nforms.I18nTextInput,
        }


class DormitoryForm(forms.ModelForm):
    class Meta:
        name = models.Dormitory
        fields = ['name', 'about',
                  'geo_longitude', 'geo_latitude', 'address',
                  'contact_name', 'contact_email', 'contact_number', 'contact_fax',
                  'cover', 'category', 'features', 'manager']
        widgets = {
            'about': i18nforms.I18nTextInput,
        }
