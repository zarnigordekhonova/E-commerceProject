from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .actions import deactivate_users
from .models import CustomUser, UserDeliveryAddres


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin configuration for CustomUser model"""
    
    list_display = ['id', 'email', 'username', 'full_name', 'is_active', 'is_confirmed', 'is_staff', 'created_at']
    list_filter = ['is_active', 'is_confirmed', 'is_staff', 'is_deleted', 'created_at']
    search_fields = ['email', 'username', 'full_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('username', 'full_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_confirmed', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at', 'deleted_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'full_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    
    readonly_fields = ['last_login', 'created_at', 'updated_at', 'deleted_at']
    filter_horizontal = ['groups', 'user_permissions']
    
    actions = ['activate_users', deactivate_users]
    
    @admin.action(description='Activate selected users')
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} user(s) activated.')
    


@admin.register(UserDeliveryAddres)
class UserDeliveryAddresAdmin(admin.ModelAdmin):
    """Admin configuration for UserDeliveryAddres model"""
    
    list_display = ['user', 'country', 'city', 'street', 'building_number', 'is_default', 'created_at']
    list_filter = ['is_default', 'country', 'city', 'created_at']
    search_fields = ['user__email', 'user__username', 'street', 'building_number']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Address Details'), {'fields': ('country', 'city', 'street', 'building_number')}),
        (_('Settings'), {'fields': ('is_default',)}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['user', 'country', 'city']
    
    actions = ['set_as_default', 'unset_as_default']
    
    @admin.action(description='Set as default address')
    def set_as_default(self, request, queryset):
        updated = queryset.update(is_default=True)
        self.message_user(request, f'{updated} address(es) set as default.')
    
    @admin.action(description='Unset as default address')
    def unset_as_default(self, request, queryset):
        updated = queryset.update(is_default=False)
        self.message_user(request, f'{updated} address(es) unset as default.')