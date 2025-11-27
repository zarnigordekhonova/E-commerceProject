from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (Category, 
                     Product, 
                     ProductComment, 
                     ProductImage, 
                     ProductRating, 
                     ProductVariant,
                     Option,
                     OptionValue,
                     ProductVariantOptionValue,
                     UserProductFavorite)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model"""
    
    list_display = ['id','category_name', 'slug', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['category_name', 'slug']
    ordering = ['id']
    
    fieldsets = (
        (_('Category Details'), {'fields': ('category_name', 'slug')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model"""
    
    list_display = ['id', 'name', 'category', 'rating', 'is_new', 'show_with_posts', 'designed_by', 'designed_year', 'created_at']
    list_filter = ['category', 'is_new', 'rating', 'show_with_posts', 'designed_year', 'created_at']
    search_fields = ['name', 'slug', 'description']
    ordering = ['name']
    
    fieldsets = (
        (_('Product Details'), {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        (_('Product Info'), {
            'fields': ('rating', 'is_new', 'designed_by', 'show_with_posts')
        }),
        (_('Timestamps'), {
            'fields': ('designed_year', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ('designed_year', 'created_at', 'updated_at')
    
    prepopulated_fields = {'slug': ('name',)}
    
    autocomplete_fields = ['category', 'designed_by']
    
    actions = ['mark_as_new', 'mark_as_old']
    
    @admin.action(description='Mark as new product')
    def mark_as_new(self, request, queryset):
        updated = queryset.update(is_new=True)
        self.message_user(request, f'{updated} product(s) marked as new.')
    
    @admin.action(description='Mark as old product')
    def mark_as_old(self, request, queryset):
        updated = queryset.update(is_new=False)
        self.message_user(request, f'{updated} product(s) marked as old.')


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """Admin configuration for ProductVariant model"""
    
    list_display = ['id', 'product', 'sku_code', 'price', 'discount_percentage', 'discount_price', 'stock_quantity', 'created_at']
    list_filter = ['product__category', 'stock_quantity', 'created_at']
    search_fields = ['product__name', 'sku_code']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Product'), {'fields': ('product',)}),
        (_('Variant Details'), {'fields': ('sku_code', 'additional_info')}),
        (_('Stock'), {'fields': ('stock_quantity',)}),
        (_('Pricing'), {'fields': ('price', 'discount_percentage')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['product']
    
    actions = ['mark_out_of_stock', 'apply_10_percent_discount', 'apply_20_percent_discount', 'remove_discount']
    
    @admin.action(description='Mark as out of stock')
    def mark_out_of_stock(self, request, queryset):
        updated = queryset.update(stock_quantity=0)
        self.message_user(request, f'{updated} variant(s) marked as out of stock.')
    
    @admin.action(description='Apply 10%% discount')
    def apply_10_percent_discount(self, request, queryset):
        updated = queryset.update(discount_percentage=10)
        self.message_user(request, f'{updated} variant(s) now have 10% discount.')

    @admin.action(description='Apply 20%% discount')
    def apply_20_percent_discount(self, request, queryset):
        updated = queryset.update(discount_percentage=20)
        self.message_user(request, f'{updated} variant(s) now have 20% discount.')
    
    @admin.action(description='Remove discount')
    def remove_discount(self, request, queryset):
        updated = queryset.update(discount_percentage=0, discount_price=0)
        self.message_user(request, f'Discount removed from {updated} variant(s).')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    """Admin configuration for Option model"""
    
    list_display = ['id', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    ordering = ['name']
    
    fieldsets = (
        (_('Option Details'), {'fields': ('name',)}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(OptionValue)
class OptionValueAdmin(admin.ModelAdmin):
    """Admin configuration for OptionValue model"""
    
    list_display = ['id', 'option', 'value', 'created_at']
    list_filter = ['option', 'created_at']
    search_fields = ['option__name', 'value']
    ordering = ['option', 'value']
    
    fieldsets = (
        (_('OptionValue Details'), {'fields': ('option', 'value')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['option']


@admin.register(ProductVariantOptionValue)
class ProductVariantOptionValueAdmin(admin.ModelAdmin):
    """Admin configuration for ProductVariantOptionValue model"""
    
    list_display = ['id', 'product_variant', 'option_value', 'created_at']
    list_filter = ['product_variant__product__category', 'created_at']
    search_fields = ['product_variant__sku_code', 'option_value__value']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Details'), {'fields': ('product_variant', 'option_value')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['product_variant', 'option_value']


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    """Admin configuration for ProductRating model"""
    
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'product', 'created_at']
    search_fields = ['user__email', 'user__username', 'product__name']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Rating Details'), {'fields': ('user', 'product', 'rating')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['user', 'product']


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    """Admin configuration for ProductComment model"""
    
    list_display = ['user', 'product', 'comment_preview', 'created_at']
    list_filter = ['product', 'created_at']
    search_fields = ['user__email', 'user__username', 'product__name', 'comment']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Comment Details'), {'fields': ('user', 'product', 'comment')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['user', 'product']
    
    @admin.display(description='Comment')
    def comment_preview(self, obj):
        """Display comment preview"""
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment


@admin.register(UserProductFavorite)
class UserProductFavoriteAdmin(admin.ModelAdmin):
    """Admin configuration for UserProductFavorite model"""
    
    list_display = ['id', 'user', 'product', 'product_name', 'created_at']
    list_filter = ['product__product__category', 'created_at']
    search_fields = ['user__email', 'user__username', 'product__product__name']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Favorite Details'), {'fields': ('user', 'product')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['user', 'product']
    
    @admin.display(description='Product Name')
    def product_name(self, obj):
        """Display product name"""
        return obj.product.product.name


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin configuration for ProductImage model"""
    
    list_display = ['id', 'product', 'product_name', 'image_preview', 'created_at']
    list_filter = ['product__product__category', 'created_at']
    search_fields = ['product__product__name', 'product__sku_code']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Image Details'), {'fields': ('product', 'image', 'image_preview')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    
    autocomplete_fields = ['product']
    
    @admin.display(description='Product Name')
    def product_name(self, obj):
        """Display product name"""
        return obj.product.product.name
    
    @admin.display(description='Preview')
    def image_preview(self, obj):
        """Display image preview"""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return '-'