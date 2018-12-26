from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from api.engine import models, forms


# Filter models

@admin.register(models.FeatureFilter)
class ModelFeatureFilterAdmin(PolymorphicChildModelAdmin):
    base_model = models.Filter
    form = forms.FeatureFilterForm


@admin.register(models.IntegralFilter)
class ModelIntegralFilterAdmin(PolymorphicChildModelAdmin):
    base_model = models.Filter
    form = forms.IntegralFilterForm


@admin.register(models.RadioFilter)
class ModelRadioFilterAdmin(PolymorphicChildModelAdmin):
    base_model = models.Filter
    form = forms.RadioFilterForm


@admin.register(models.Filter)
class ModelFilterAdmin(PolymorphicParentModelAdmin):
    child_models = (models.FeatureFilter, models.IntegralFilter, models.RadioFilter)

# Choice models


@admin.register(models.IntegralChoice)
class ModelIntegralChoiceAdmin(PolymorphicChildModelAdmin):
    base_model = models.Choice


@admin.register(models.RadioChoice)
class ModelRadioChoiceAdmin(PolymorphicChildModelAdmin):
    base_model = models.Choice


@admin.register(models.Choice)
class ModelChoiceParentAdmin(PolymorphicParentModelAdmin):
    child_models = (models.IntegralChoice, models.RadioChoice)


# Dormitory models

class DormitoryCategoryAdmin(admin.ModelAdmin):
    form = forms.DormitoryCategoryForm


class DormitoryAdmin(admin.ModelAdmin):
    form = forms.DormitoryForm


admin.site.register(models.Dormitory, DormitoryAdmin)
admin.site.register(models.DormitoryCategory, DormitoryCategoryAdmin)
admin.site.register(models.BankAccount)
admin.site.register(models.DormitoryPhoto)


# User
class CustomUserAdmin(UserAdmin):
    # as an example, this custom user admin orders users by email address
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        ('Custom fields', {'fields': ('is_manager', )}),
    )


admin.site.register(models.User, CustomUserAdmin)

# Other models


class RadioOptionAdmin(admin.ModelAdmin):
    form = forms.RadioOptionForm


admin.site.register(models.RadioOption, RadioOptionAdmin)

admin.site.register(models.Currency)


admin.site.register(models.RoomCharacteristics)
admin.site.register(models.RoomPhoto)

admin.site.register(models.Reservation)
admin.site.register(models.Review)
admin.site.register(models.ReceiptPhoto)
