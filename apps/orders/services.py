from django.core.cache import cache
from decimal import Decimal

from apps.products.models import ProductVariant


def add_to_cart(user, product, quantity=1):
    """Add product to cached cart"""
    cart_key = f'cart_{user.id}'
    cart = cache.get(cart_key, {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + quantity
    cache.set(cart_key, cart, 86400 * 14) # cart expiration days

def get_cart(user):
    """Get cached cart"""
    cart_key = f'cart_{user.id}'
    return cache.get(cart_key, {})

def get_cart_total_price(user):
    """Calculate total price from cache"""
    cart_key = f'cart_{user.id}'
    cart = cache.get(cart_key, {})
    total = Decimal('0.00')
    for product_id, qty in cart.items():
        product = ProductVariant.objects.get(id=product_id)
        total += product.price * qty
    return total

def get_cart_item_count(user):
    """Get number of different products in cart"""
    cart = get_cart(user)
    return len(cart)  # Returns number of unique products

def get_cart_item_count(user):
    """Get number of different products in cart"""
    cart = get_cart(user)
    return len(cart)  # Returns overall number of products

def clear_cart(user):
    """Clear cart from cache"""
    cache_key = f'cart_{user.id}'
    cache.delete(cache_key)