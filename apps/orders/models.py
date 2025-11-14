from django.db import models
from django.db import transaction, IntegrityError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from decimal import Decimal

from .utils import generate_order_number
from apps.common.models import BaseModel


class ShoppingCart(BaseModel):
    user = models.OneToOneField("accounts.CustomUser",
                             on_delete=models.CASCADE,
                             related_name="cart",
                             verbose_name=_("User Shopping cart"))
    
    @property
    def total_price(self):
        return sum((item.subtotal for item in self.items.all()), Decimal("0.00"))
    
    @property
    def item_quantities(self):
        """Dict of products and their quantities in the cart"""
        return {item.product.name: item.quantity for item in self.items.all()}
    
    @property
    def is_empty(self):
        """Check if cart has no items"""
        return not self.items.exists()
    
    def clear(self):
        """Remove all items from cart"""
        self.items.all().delete()
    
    def add_product(self, product, quantity=1):
        """Add a product to cart or update quantity if already exists"""
        cart_item, created = self.items.get_or_create(
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item

    def __str__(self):
        return f"Shopping Cart of {self.user.username}" 
    
    class Meta:
        verbose_name = _("Shopping Cart")
        verbose_name_plural = _("Shopping Carts")
   

class ShoppingCartItem(BaseModel):
    cart = models.ForeignKey(ShoppingCart,
                             on_delete=models.CASCADE,
                             related_name="items",
                             verbose_name=_("Shopping cart"))
    product = models.ForeignKey("products.ProductVariant",
                                 on_delete=models.CASCADE,
                                 related_name="cart_items",
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
            models.UniqueConstraint(fields=["cart", "product"], name="unique_cart_product"),
        )


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

    user = models.ForeignKey("accounts.CustomUser",
                             on_delete=models.CASCADE,
                             related_name="orders",
                             verbose_name=_("Order User"))
    order_number = models.CharField(max_length=20, 
                                    unique=True, 
                                    verbose_name=_("Order Number"))
    cart = models.ForeignKey(ShoppingCart,
                            on_delete=models.CASCADE,
                            related_name="order_cart",
                            verbose_name=_("Order cart"))
    total = models.DecimalField(max_digits=10,
                                decimal_places=2,  
                                verbose_name=_("Order Total"),
                                default=Decimal('0.00'))
    status = models.CharField(max_length=20,
                              choices=OrderStatus.choices,  
                              default=OrderStatus.PENDING,
                              verbose_name=_("Order Status"))
    shipping_type = models.CharField(max_length=20,
                                      choices=ShippingType.choices,
                                      default=ShippingType.FREE,
                                      verbose_name=_("Shipping Type"))
    shipping_cost = models.DecimalField(max_digits=8,
                                        decimal_places=2,
                                        verbose_name=_("Shipping Cost"),
                                        default=Decimal('0.00'))
    
    def save(self, *args, **kwargs):
        if self.cart:
            self.total = self.cart.total_price
        elif hasattr(self.user, 'cart') and self.user.cart:
            self.total = self.user.cart.total_price

        if not self.order_number:
            max_attempts = 5
            for attempt in range(max_attempts):
                order_number = generate_order_number()
                self.order_number = f"ORD{order_number}"
                try:
                    with transaction.atomic():
                        super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    if attempt == max_attempts-1:
                        raise 
        else:
            super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"
    
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created_at']


class OrderDetail(BaseModel):

    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'CREDIT_CARD', _("Credit Card")
        PAYPAL = 'PAYPAL', _("PayPal")
        CASH_ON_DELIVERY = 'CASH_ON_DELIVERY', _("Cash on Delivery")

    order =  models.ForeignKey(Order,
                               on_delete=models.CASCADE,
                               related_name="order_details",
                               verbose_name=_("Order"))
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
    payment_method = models.CharField(max_length=50, 
                                      choices=PaymentMethod.choices,
                                      default=PaymentMethod.PAYPAL,
                                      verbose_name=_("Payment Method"))
    
    def __str__(self):
        return f"Order Detail for {self.order.order_number}"
    
    class Meta:
        verbose_name = _("Order Detail")
        verbose_name_plural = _("Order Details")
    
    
   