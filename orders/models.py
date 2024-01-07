from django.contrib.auth.models import User
from django.db import models

from basket.models import Basket
from customers.abstract_model import TimeStamp



class ShippingAddress(TimeStamp):
    line_1 = models.CharField(max_length=250)
    line_2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='shipping_address', null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.line_1}-{self.user.username}"

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"
        unique_together = ('line_1', 'line_2', 'city', 'postcode')

    @property
    def full_address(self):
        return f"{self.line_1}, {self.line_2}, {self.city}, {self.postcode}"


class Order(TimeStamp):
    CASH_ON_DELIVERY = 'cash_on_delivery'
    ONLINE_TRANSACTION = 'online_transaction'
    PAYMENT_METHOD = ((CASH_ON_DELIVERY, "Cash on Delivery"), (ONLINE_TRANSACTION, "Online Transaction"))
    PLACED = 'placed'
    PACKED = 'packed'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    STATUS = ((PLACED, "Placed"), (PACKED, "Packed"), (SHIPPED, "Shippped"), (DELIVERED, "Delivered"))
    status = models.CharField(max_length=30, default=PLACED, choices=STATUS)
    number = models.CharField(max_length=10, unique=True)
    basket = models.ForeignKey(Basket, on_delete=models.SET_NULL, related_name='orders', null=True)
    total_incl_tax = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_orders', null=True)
    payment_method = models.CharField(choices=PAYMENT_METHOD, default=ONLINE_TRANSACTION, max_length=30)
    transaction_id = models.CharField(max_length=250, null=True, blank=True)
    notes = models.TextField(blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


    def __str__(self):
        return self.number



