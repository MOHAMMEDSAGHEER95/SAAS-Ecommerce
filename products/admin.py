from django.contrib import admin

# Register your models here.
from products.models import Products, Brand

admin.site.register(Products)
admin.site.register(Brand)
