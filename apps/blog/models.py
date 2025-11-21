from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.products.utils import make_slug


class Post(BaseModel):
    title = models.CharField(max_length=255,
                            verbose_name=_("Title"),
                            help_text=_("Enter the title of the blog post."),
                            unique=True
                            )
    slug = models.SlugField(max_length=255,
                            unique=True,
                            verbose_name=_("Slug"),
                            blank=True
                            )
    # In Figma design, it looks like this => DE - Hamburg, 2022 | Office
    short_description = models.CharField(max_length=255,
                                         verbose_name=_("Short description")) 
    description = models.TextField(verbose_name=_("Description"))   
    main_image = models.ForeignKey("PostImage",
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   related_name="main_post_image")
    products = models.ManyToManyField("products.Product",
                                      related_name="posts",
                                      verbose_name=_("Related Products"),
                                      blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = make_slug(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

class PostImage(BaseModel):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="images", # changed from "posts" to "images"
                             verbose_name=_("Post")
                             )
    
    image =  models.ImageField(upload_to="post_images/",
                               null=True,
                               blank=True,
                               verbose_name=_("Post images"))
    
    def __str__(self):
        return f"{self.post} - Image {self.id}"
    
    class Meta:
        verbose_name = _("Post Image")
        verbose_name_plural = _("Post Images")
 
        