from django.db import models
from djrichtextfield.models import RichTextField

from customers.abstract_model import TimeStamp
from products.models import get_upload_path


# Create your models here.


class BannerImages(TimeStamp):
    image = models.ImageField(upload_to=get_upload_path, null=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "Banner Image"
        verbose_name_plural = "Banner Images"


class Blog(TimeStamp):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published')
    ]
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to=get_upload_path, null=True)
    body = RichTextField()
    status = models.CharField(choices=STATUS_CHOICES, default=DRAFT, max_length=60)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"




