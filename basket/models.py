from django.contrib.auth.models import User
from django.db import models

from customers.abstract_model import TimeStamp
from products.models import Products


# Create your models here.

class Basket(TimeStamp):
    OPEN, SUBMITTED = ("Open", "Submitted")
    STATUS = (
        (OPEN, "Open - currently active"),
        (SUBMITTED, "Submitted - has been ordered at the checkout"),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(choices=STATUS, default=OPEN, max_length=100)
    submitted_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id)

    def total(self):
        sum = 0
        for line in self.lines.all():
            sum += line.price * line.quantity
        return sum


class BasketLine(TimeStamp):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="products")
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        verbose_name = "Line"
        verbose_name_plural = "Lines"

    def __str__(self):
        return f"{self.product.__str__()}-{self.quantity}"




