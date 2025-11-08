from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import City, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Admin configuration for Country model"""
    
    list_display = ['country_name', 'code', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['country_name', 'code']
    ordering = ['country_name']
    
    fieldsets = (
        (_('Country Details'), {'fields': ('country_name', 'code')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Admin configuration for City model"""
    
    list_display = ['city_name', 'country', 'created_at', 'updated_at']
    list_filter = ['country', 'created_at']
    search_fields = ['city_name', 'country__country_name', 'country__code']
    ordering = ['city_name']
    
    fieldsets = (
        (_('City Details'), {'fields': ('city_name', 'country')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['country']