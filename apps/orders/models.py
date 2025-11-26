from django.db import models
from django.db import transaction, IntegrityError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from decimal import Decimal

from .utils import generate_order_number
from apps.common.models import BaseModel
   

class ShoppingCartItem(BaseModel):
    user = models.ForeignKey("accounts.CustomUser",
                             on_delete=models.CASCADE,
                             related_name="cart_items",
                             verbose_name=_("User"))
    product = models.ForeignKey("products.ProductVariant",
                                 on_delete=models.CASCADE,
                                 related_name="cart_products",
                                 verbose_name=_("Shopping cart items"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Product quantity"))

    @property
    def subtotal(self):
        """Function for calculating product subtotal price"""
        price = self.product.price or Decimal('0.00')
        quantity = self.quantity or 0
        return price * quantity
    
    @property
    def is_in_stock(self):
        return self.product.stock_quantity >= self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product}"
    
    class Meta:
        verbose_name = _("Shopping Cart Item")
        verbose_name_plural = _("Shopping Cart Items")
        ordering = ['-created_at']
        constraints = (
            models.UniqueConstraint(fields=["user", "product"], name="unique_user_product"),
        )


# Merged with OrderDetail model
class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', _("Pending")
        PROCESSING = 'PROCESSING', _("Processing")
        SHIPPING = 'SHIPPING', _("Shipping")
        DELIVERED = 'DELIVERED', _("Delivered")
        CANCELED = 'CANCELED', _("Canceled")
        REFUNDED = 'REFUNDED', _("Refunded")

    class ShippingType(models.TextChoices):
        FREE = 'FREE', _("Free Shipping")
        EXPRESS = 'EXPRESS', _("Express Shipping")
        PICKUP = 'PICKUP', _("Store Pickup")

    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'CREDIT_CARD', _("Credit Card")
        PAYPAL = 'PAYPAL', _("PayPal")
        CASH_ON_DELIVERY = 'CASH_ON_DELIVERY', _("Cash on Delivery")

#   ============ ORDER DETAILS ==============

    user = models.ForeignKey("accounts.CustomUser",
                            on_delete=models.CASCADE,
                            related_name="orders",
                            verbose_name=_("Order User"))
    order_number = models.CharField(max_length=50, 
                                    unique=True, 
                                    verbose_name=_("Order Number"))
    
#   ============ PRICING and SHIPPING ============

    total_price = models.DecimalField(max_digits=10,
                                decimal_places=2,  
                                verbose_name=_("Order's Total Price"),
                                default=Decimal('0.00'))
    shipping_type = models.CharField(max_length=20,
                                    choices=ShippingType.choices,
                                    default=ShippingType.FREE,
                                    verbose_name=_("Shipping Type"))
    shipping_cost = models.DecimalField(max_digits=8,
                                        decimal_places=2,
                                        verbose_name=_("Shipping Cost"),
                                        default=Decimal('0.00'))
    
#   ============ ORDER STATUS ================

    status = models.CharField(max_length=20,
                            choices=OrderStatus.choices,  
                            default=OrderStatus.PENDING,
                            verbose_name=_("Order Status"))
    
#   ============ USER DETAILS =============

    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    phone_number = models.CharField(
        max_length=50,  
        validators=[
            RegexValidator(
                regex=r"^\+998\d{9}$",
            )
        ],
        verbose_name=_("Phone number"))
    email = models.EmailField(verbose_name=_("Email Address"))

#   ============ ADDRESS DETAILS ============

    country = models.ForeignKey("common.Country",
                                on_delete=models.CASCADE,
                                verbose_name=_("Country"))
    city = models.ForeignKey("common.City",
                             on_delete=models.CASCADE,
                             verbose_name=_("City"))
    state = models.CharField(max_length=100, 
                             null=True,
                             blank=True,
                             verbose_name=_("State/Province"))
    street = models.CharField(max_length=255, verbose_name=_("Street Address"))
    zip_code = models.CharField(max_length=20, verbose_name=_("Postal Code"))

#   ============ PAYMENT METHOD =============

    payment_method = models.CharField(max_length=50, 
                                      choices=PaymentMethod.choices,
                                      default=PaymentMethod.PAYPAL,
                                      verbose_name=_("Payment Method"))
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD{generate_order_number()}"
        super().save(*args, **kwargs)

    def calculate_total(self):
        items_total_price = sum(item.get_subtotal() for item in self.items.all())

        if self.shipping_type != self.ShippingType.FREE:
            self.total_price = items_total_price + self.shipping_cost
        else:
            self.total_price = items_total_price
        return self.total_price
    
    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"
    
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created_at']


class OrderItem(BaseModel):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name="items",
                              verbose_name=_("Order"))
    product = models.ForeignKey("products.ProductVariant",
                                on_delete=models.CASCADE,
                                related_name="order_items",
                                verbose_name=_("ProductVariant"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Product Quantity"))
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name=_("Product Price"))
    
    def get_subtotal(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity}x {self.product} in Order {self.order.order_number}"
    
    class Meta:
        verbose_name = _("OrderItem")
        verbose_name_plural = ("OrderItems")
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"], name="unique_product_order"
            )
        ]

