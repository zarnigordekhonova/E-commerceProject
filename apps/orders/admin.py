from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import ShoppingCart, ShoppingCartItem, Order, OrderDetail


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Admin configuration for ShoppingCart model"""
    
    list_display = ['user', 'total_price', 'item_count', 'is_empty', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__email', 'user__username', 'user__full_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Cart Details'), {'fields': ('user',)}),
        (_('Cart Info'), {'fields': ('total_price', 'item_count', 'is_empty')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'total_price', 'item_count', 'is_empty']
    
    autocomplete_fields = ['user']
    
    actions = ['clear_carts']
    
    @admin.display(description='Total Items')
    def item_count(self, obj):
        """Display total number of items in cart"""
        return obj.items.count()
    
    @admin.action(description='Clear selected carts')
    def clear_carts(self, request, queryset):
        count = 0
        for cart in queryset:
            cart.clear()
            count += 1
        self.message_user(request, f'{count} cart(s) cleared.')


@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    """Admin configuration for ShoppingCartItem model"""
    
    list_display = ['cart', 'product', 'quantity', 'subtotal', 'is_in_stock', 'created_at']
    list_filter = ['created_at', 'cart']
    search_fields = ['cart__user__email', 'cart__user__username', 'product__name']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Cart Item Details'), {'fields': ('cart', 'product', 'quantity')}),
        (_('Item Info'), {'fields': ('subtotal', 'is_in_stock')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'subtotal', 'is_in_stock']
    
    autocomplete_fields = ['cart', 'product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model"""
    
    list_display = ['order_number', 'user', 'status_badge', 'shipping_type', 'total', 'shipping_cost', 'created_at']
    list_filter = ['status', 'shipping_type', 'created_at', 'updated_at']
    search_fields = ['order_number', 'user__email', 'user__username']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Order Details'), {'fields': ('user', 'order_number', 'cart')}),
        (_('Pricing'), {'fields': ('total', 'shipping_cost')}),
        (_('Status & Shipping'), {'fields': ('status', 'shipping_type')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'order_number', 'total']
    
    autocomplete_fields = ['user', 'cart']
    
    actions = ['mark_as_processing', 'mark_as_shipping', 'mark_as_delivered', 'mark_as_canceled']
    
    @admin.display(description='Status', ordering='status')
    def status_badge(self, obj):
        """Display colored status badge"""
        colors = {
            'PENDING': '#ffc107',
            'PROCESSING': '#17a2b8',
            'SHIPPING': '#007bff',
            'DELIVERED': '#28a745',
            'CANCELED': '#dc3545',
            'REFUNDED': '#6c757d',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    
    @admin.action(description='Mark as Processing')
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status=Order.OrderStatus.PROCESSING)
        self.message_user(request, f'{updated} order(s) marked as Processing.')
    
    @admin.action(description='Mark as Shipping')
    def mark_as_shipping(self, request, queryset):
        updated = queryset.update(status=Order.OrderStatus.SHIPPING)
        self.message_user(request, f'{updated} order(s) marked as Shipping.')
    
    @admin.action(description='Mark as Delivered')
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status=Order.OrderStatus.DELIVERED)
        self.message_user(request, f'{updated} order(s) marked as Delivered.')
    
    @admin.action(description='Mark as Canceled')
    def mark_as_canceled(self, request, queryset):
        updated = queryset.update(status=Order.OrderStatus.CANCELED)
        self.message_user(request, f'{updated} order(s) marked as Canceled.')


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    """Admin configuration for OrderDetail model"""
    
    list_display = ['order', 'full_name', 'email', 'phone_number', 'country', 'city', 'payment_method', 'created_at']
    list_filter = ['payment_method', 'country', 'city', 'created_at']
    search_fields = ['order__order_number', 'first_name', 'last_name', 'email', 'phone_number', 'street']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Order'), {'fields': ('order',)}),
        (_('Personal Information'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Address'), {'fields': ('country', 'city', 'state', 'street', 'zip_code')}),
        (_('Payment'), {'fields': ('payment_method',)}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['order', 'country', 'city']
    
    @admin.display(description='Full Name')
    def full_name(self, obj):
        """Display full name"""
        return f"{obj.first_name} {obj.last_name}"


