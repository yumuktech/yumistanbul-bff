from django.contrib import admin

from .models import AdditionalFilter, District, FeatureTag, Restaurant


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FeatureTag)
class FeatureTagAdmin(admin.ModelAdmin):
    list_display = ('key', 'label')


@admin.register(AdditionalFilter)
class AdditionalFilterAdmin(admin.ModelAdmin):
    list_display = ('key', 'label', 'emoji')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'price_tier', 'rating', 'is_active')
    list_filter = ('district', 'is_active', 'price_tier')
    search_fields = ('name', 'description', 'district__name')
    filter_horizontal = ('features', 'additional_filters')
    prepopulated_fields = {'slug': ('name',)}
