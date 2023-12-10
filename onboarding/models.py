from django.db import models

# Create your models here.
from customers.abstract_model import TimeStamp


class Plan(TimeStamp):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

    def __str__(self):
        return self.title

    def decription_array(self):
        return self.description.split("*")
