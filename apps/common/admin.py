from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import City, Country, Designer, NewsLetter


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Admin configuration for Country model"""
    
    list_display = ['id', 'name', 'code', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['name', 'code']
    ordering = ['name']
    
    fieldsets = (
        (_('Country Details'), {'fields': ('name', 'code')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Admin configuration for City model"""
    
    list_display = ['id', 'name', 'country', 'created_at', 'updated_at']
    list_filter = ['country', 'created_at']
    search_fields = ['name', 'country__country_name', 'country__code']
    ordering = ['name']
    
    fieldsets = (
        (_('City Details'), {'fields': ('name', 'country')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['country']


@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    """Admin configuration for Designer model"""
    
    list_display = ['id', 'full_name', 'designer_image', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['full_name']
    ordering = ['id']
    
    fieldsets = (
        (_('Designer Details'), {'fields': ('full_name', 'designer_image')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    """Admin configuration for NewsLetter model"""
    
    list_display = ['id', 'email', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['email']
    ordering = ['id']
    
    fieldsets = (
        (_('NewsLetter Details'), {'fields': ('email', )}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
