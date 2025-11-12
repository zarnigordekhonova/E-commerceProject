from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg

from apps.products.models import ProductRating


@receiver(post_save, sender=ProductRating)
def update_product_rating(sender, instance, created, **kwargs):
    product = instance.product

    average_rating = (
        ProductRating.objects.
        filter(product=product).
        aggregate(avg_rating=Avg('rating'))['avg_rating']
    )

    if average_rating is not None:
        product.rating = round(average_rating, 2)
    else:
        product.rating = 0.0
    
    product.save(update_fields=['rating'])
    print("AVG_RATING:", average_rating)