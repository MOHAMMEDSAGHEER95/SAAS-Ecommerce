from django.db import models

# Create your models here.


class Charges(models.Model):
    price = models.IntegerField()
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Charges'

    def __str__(self):
        return self.description
