from django.contrib import admin

from basket.models import Basket, BasketLine

# Register your models here.
admin.site.register(Basket)
admin.site.register(BasketLine)
