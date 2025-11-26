from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from decimal import Decimal

from .utils import make_slug
from apps.common.models import BaseModel


class Category(BaseModel):
    category_name = models.CharField(max_length=64, 
                                     verbose_name=_("Category name"),
                                     unique=True,
                                     db_index=True)
    slug = models.SlugField(max_length=64,
                            verbose_name=_("Slug"),
                            unique=True)
    
    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = make_slug(self.category_name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['category_name']


class Product(BaseModel):
    name = models.CharField(max_length=128,
                            verbose_name=_("Product name"))
    slug = models.SlugField(max_length=128,
                            verbose_name=_("Slug"),
                            unique=True,
                            blank=True)
    description = models.TextField(verbose_name=_("Description"))
    rating = models.FloatField(verbose_name=_("Rating"), 
                               default=0)
    is_new = models.BooleanField(verbose_name=_("Is new product"),
                                 default=False)
    designed_year = models.DateField(auto_now_add=True,
                                     verbose_name=_("Product designed year"))
    designed_by = models.ForeignKey("common.Designer",
                                    on_delete=models.DO_NOTHING,
                                    related_name="product_designers",
                                    verbose_name=_("Product designer"))
    category = models.ForeignKey(Category, 
                                 on_delete=models.CASCADE, 
                                 related_name='products',
                                 verbose_name=_("Category"))
    show_with_posts = models.BooleanField(default=False,
                                          verbose_name=_("Products with Posts"))
    
    def __str__(self):
        return f"{self.name} - {self.designed_year} - {self.show_with_posts}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = make_slug(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['name']
        indexes = [
            models.Index(fields=["category", "rating"])
        ]
        # Prevents duplicate product names and slugs within the same category
        constraints = [
            models.UniqueConstraint(fields=['slug', 'category'], name='unique_slug_in_category'),
            models.UniqueConstraint(fields=['name', 'category'], name='unique_product_in_category')
        ]
        
    
class ProductVariant(BaseModel):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='variants',
                                verbose_name=_("Product variant"))
    additional_info = models.TextField(null=True,
                                       blank=True,
                                       verbose_name=_("Additional information"))
    sku_code = models.CharField(max_length=64,
                                verbose_name=_("SKU code"),
                                unique=True)
    stock_quantity = models.PositiveIntegerField(verbose_name=_("Stock quantity"),
                                                default=0)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,   
                                verbose_name=_("Product price"))
    discount_price = models.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         verbose_name=_("Discount price"),
                                         default=Decimal("0.00"))
    discount_percentage = models.FloatField(verbose_name=_("Discount percentage"),
                                            default=0)
    
    def __str__(self):
        return f"{self.product.name}"
    
    def save(self, *args, **kwargs):
        if self.discount_percentage > 0:
            discount_amount = self.price * (Decimal(self.discount_percentage) / 100)
            self.discount_price = self.price - discount_amount
            self.discount_price = self.discount_price.quantize(Decimal('0.01'))
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")
        indexes = [
            models.Index(fields=["sku_code", "price"])
            ]
        

class Option(BaseModel):
    name = models.CharField(max_length=32,
                            verbose_name=_("Option name")) 
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, *kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Option")
        verbose_name_plural = _("Options") 
        constraints = [
            models.UniqueConstraint(fields=['name'], name="unique_option_name")
        ]


class OptionValue(BaseModel):
    option = models.ForeignKey(Option,
                               on_delete=models.CASCADE,
                               verbose_name=_("Option's value"))
    value = models.CharField(max_length=32,
                             verbose_name=_("Value"))
    
    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = _("OptionValue")
        verbose_name_plural = _("OptionValues")
        constraints = [
            models.UniqueConstraint(
                fields=["option", "value"], name="unique_option_value"
            )
        ]


class ProductVariantOptionValue(BaseModel):
    product_variant = models.ForeignKey(ProductVariant,
                                        on_delete=models.CASCADE,
                                        related_name="variant_options",
                                        verbose_name=_("Product Variant"))
    option_value = models.ForeignKey(OptionValue,
                                     on_delete=models.CASCADE,
                                     verbose_name=_("Product's Option and Value"))
    
    def __str__(self):
        return f"{self.product_variant} - {self.option_value}"
    
    class Meta:
        verbose_name = _("ProductVariantOptionValue")
        verbose_name_plural = _("ProductVariantOptionValues")
        constraints = [
            models.UniqueConstraint(
                fields=["product_variant", "option_value"], name="unique_product_variant_option_value"
            )
        ]
        

class ProductRating(BaseModel):
    user = models.ForeignKey("accounts.CustomUser",
                             on_delete=models.CASCADE,
                             related_name="ratings",
                             verbose_name=_("User rating"))
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="product_rating",
                                verbose_name=_("Product rating"))
    rating = models.FloatField(verbose_name=_("Rating"), 
                               validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}"
    
    class Meta:
        verbose_name = _("Product Rating")
        verbose_name_plural = _("Product Ratings")
        ordering = ['-created_at']


class ProductComment(BaseModel):
    user = models.ForeignKey("accounts.CustomUser",
                             on_delete=models.CASCADE,
                             related_name="comments",
                             verbose_name=_("User comment"))
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="product_comment",
                                verbose_name=_("Product comment"))
    comment = models.TextField(verbose_name=_("Comment"))

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.comment[:20]}"
    
    class Meta:
        verbose_name = _("Product Comment")
        verbose_name_plural = _("Product Comments")
        ordering = ['-created_at']


class UserProductFavorite(BaseModel):
    user = models.ForeignKey("accounts.CustomUser",
                             on_delete=models.CASCADE,
                             related_name="favorite_products",
                             verbose_name=_("User favorite"))
    product = models.ForeignKey(ProductVariant,
                                on_delete=models.CASCADE,
                                related_name="favorited_by",
                                verbose_name=_("Product favorite"))
    
    def __str__(self):
        return f"{self.user.username} - {self.product.product.name}"
    
    class Meta:
        verbose_name = _("User Product Favorite")
        verbose_name_plural = _("User Product Favorites")
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product_favorite')]
        ordering = ['-created_at']


class ProductImage(BaseModel):
    product = models.ForeignKey(ProductVariant,
                                on_delete=models.CASCADE,
                                related_name="images",
                                verbose_name=_("Product image"))
    image = models.ImageField(upload_to='product_images/',
                              verbose_name=_("Image"))
    
    def __str__(self):
        return f"{self.product.product.name} - Image {self.id}"
    
    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ['-created_at']  



