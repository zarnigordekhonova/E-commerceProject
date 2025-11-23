from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save

from apps.common.models import NewsLetter


@receiver(post_save, sender=NewsLetter)
def send_newsletter_confirmation_email(sender, instance, created, **kwargs):
    
    if created:  
        subject = "Welcome to Our Newsletter!"
        
        message = f"""
                    Hello,

                    Thank you for subscribing to our newsletter!

                    You are now subscribed with the email: {instance.email}

                    You will receive updates about:
                    - New products and discounts
                    - Exclusive offers
                    - Latest news from our store

                    If you wish to unsubscribe, you can do so by replying to this email or visiting our website.

                    Best regards,
                    The E-Commerce Team
                """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )


__all__ = [
    "send_newsletter_confirmation_email"
]