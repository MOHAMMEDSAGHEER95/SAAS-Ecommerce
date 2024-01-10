from django.contrib import admin

# Register your models here.
from products.models import Products, Brand, Category

admin.site.register(Products)
admin.site.register(Brand)
admin.site.register(Category)
