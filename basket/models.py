from django.contrib.auth.models import User
from django.db import models

from customers.abstract_model import TimeStamp
from products.models import Products


# Create your models here.

class Basket(TimeStamp):
    OPEN, SUBMITTED, MERGED = ("Open", "Submitted", "Merged")
    STATUS = (
        (OPEN, "Open - currently active"),
        (SUBMITTED, "Submitted - has been ordered at the checkout"),
        (MERGED, "Merged - has been merged with old basket"),
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
    @classmethod
    def create_basket(self, user):
        if user.is_authenticated:
            basket = Basket.objects.create(user=user)
            return basket
        basket  = Basket.objects.create()
        return basket

    @classmethod
    def get_basket(self, user):
        basket = user.basket_set.last()
        if basket.status == basket.OPEN:
            return basket
        else:
            return self.create_basket(user)

    def create_basket_lines(self, product_id, quantity):
        product = Products.objects.get(id=product_id)
        if int(quantity) == 0:
            self.lines.filter(product_id=product_id).delete()
        elif self.lines.filter(product_id=product_id).exists():
            price = int(quantity) * product.price
            self.lines.filter(product_id=product_id).update(quantity=int(quantity), price=price)
        else:
            line = BasketLine.objects.create(basket=self, product_id=product_id, quantity=int(quantity),
                                             price=product.price)
        return self.lines.count()

    def merge_basket_lines(self, product_id, quantity):
        product = Products.objects.get(id=product_id)
        if int(quantity) == 0:
            self.lines.filter(product_id=product_id).delete()
        elif self.lines.filter(product_id=product_id).exists():
            orginal_quantity = self.lines.filter(product_id=product_id).first().quantity
            quantity += orginal_quantity
            price = int(quantity) * product.price
            self.lines.filter(product_id=product_id).update(quantity=int(quantity), price=price)
        else:
            line = BasketLine.objects.create(basket=self, product_id=product_id, quantity=int(quantity),
                                             price=product.price)
        return self.lines.count()

    @classmethod
    def merge_basket(cls, old_basket_id, new_basket_id):
        if old_basket_id != new_basket_id:
            old_basket = Basket.objects.get(id=old_basket_id)
            new_basket = Basket.objects.get(id=new_basket_id)
            if old_basket.status != Basket.MERGED:
                for line in old_basket.lines.all():
                    new_basket.merge_basket_lines(line.product_id, line.quantity)
                old_basket.status = Basket.MERGED
                old_basket.save()

    def get_product_line_count(self, product_id):
        if self.lines.filter(product_id=product_id).exists():
            return self.lines.filter(product_id=product_id).first().quantity
        return 0


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




