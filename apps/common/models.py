from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class Country(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_("Country Name"))
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Country Code"))

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return f"{self.name} - {self.code}"
    

class City(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_("City Name"))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities", verbose_name=_("Country"))

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return f"{self.name}, {self.country.code}"
    

class Designer(BaseModel):
     full_name = models.CharField(max_length=128,
                                  unique=True,
                                  verbose_name=_("Product designer"))
     designer_image = models.ImageField(upload_to="designers/", 
                                        null=True,
                                        blank=True,
                                        verbose_name=_("Designer image"))

     class Meta:
         verbose_name = _("Designer")
         verbose_name_plural = _("Designers")

     def __str__(self):
         return self.full_name        