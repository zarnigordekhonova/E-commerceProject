from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Post, PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for Post model"""
    
    list_display = ['title', 'slug', 'short_description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'slug', 'short_description', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Post Content'), {'fields': ('title', 'slug', 'short_description', 'description')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    prepopulated_fields = {'slug': ('title',)}


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    """Admin configuration for PostImage model"""
    
    list_display = ['id', 'post', 'image_preview', 'created_at']
    list_filter = ['created_at', 'post']
    search_fields = ['post__title', 'post__slug']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Image Details'), {'fields': ('post', 'image', 'image_preview')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    
    autocomplete_fields = ['post']
    
    @admin.display(description='Preview')
    def image_preview(self, obj):
        """Display image preview"""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return '-'