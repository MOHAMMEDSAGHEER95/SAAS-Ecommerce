from django.contrib import admin

# Register your models here.
from products.models import Products

admin.site.register(Products)
