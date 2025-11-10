from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils import timezone

from apps.common.models import BaseModel
from apps.accounts.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    full_name = models.CharField(max_length=256,
                                 verbose_name=_("Full name"),
                                 help_text=_("User's full name"))
    username = models.CharField(max_length=128,
                                verbose_name=_("Username"),
                                unique=True,
                                db_index=True)
    email = models.EmailField(max_length=128,
                              verbose_name=_("User email"),
                              unique=True,
                              db_index=True)
    is_active = models.BooleanField(default=True,
                                    verbose_name=_("Active status"),
                                    db_index=True)
    is_confirmed = models.BooleanField(default=False, verbose_name=_("Is Confirmed"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=_("Deleted status"),
                                     db_index=True)
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Deleted at"),
        help_text=_("Timestamp when user was deleted")
    )
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username", 
        "full_name",
    ]

    def __str__(self):
        if self.full_name:
            return f"{self.email} - {self.full_name}"
        return self.email
    
    class Meta:
        verbose_name = _("CustomUser")
        verbose_name_plural = _("CustomUsers")
        constraints = [
            models.UniqueConstraint(
                fields=["username"],
                condition=models.Q(is_deleted=False),
                name="unique_active_username",
            ),
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(is_deleted=False),
                name="unique_active_email",
            ),
        ]

    def delete_account(self):
        """Soft delete user account"""
        timestamp = int(timezone.now().timestamp())
        
        max_email_length = 128 - len(f"_deleted_{timestamp}") - 1
        base_email = self.email[:max_email_length] if len(self.email) > max_email_length else self.email
        
        max_username_length = 128 - len(f"_del_{timestamp}") - 1
        base_username = self.username[:max_username_length] if len(self.username) > max_username_length else self.username
        
        self.email = f"{base_email}_deleted_{timestamp}"
        self.username = f"{base_username}_del_{timestamp}"
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = timezone.now()
        
        self.save(update_fields=["email", "username", "is_deleted", "is_active", "deleted_at"])


class UserDeliveryAddres(BaseModel):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name="delivery_addresses",
                             verbose_name=_("User"))
    country = models.ForeignKey("common.Country",
                                on_delete=models.CASCADE,
                                verbose_name=_("Delivery country"))
    city = models.ForeignKey("common.City",
                             on_delete=models.CASCADE,
                             verbose_name=_("Delivery city"))
    street = models.CharField(max_length=128, verbose_name=_("Delivery street"))
    building_number = models.CharField(max_length=64, verbose_name=_("Delivery building number"))
    is_default = models.BooleanField(default=False,
                                     verbose_name=_("Default Address"),
                                     db_index=True)

    def __str__(self):
        return f"{self.user.username} - {self.is_default}"
    
    class Meta:
        verbose_name = _("User Delivery Address")
        verbose_name_plural = _("User Delivery Addresses")
    