import os

from django.db import models, connection

# Create your models here.
from customers.abstract_model import TimeStamp


def get_upload_path(instance, filename):
    return os.path.join(connection.schema_name, filename)


class Products(TimeStamp):
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to=get_upload_path, null=True)
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    url = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title
