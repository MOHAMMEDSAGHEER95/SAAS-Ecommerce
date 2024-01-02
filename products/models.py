import os

from django.db import models, connection
from django_extensions.db.fields import AutoSlugField
from tenant_schemas.utils import schema_context


# Create your models here.
from customers.abstract_model import TimeStamp


def get_upload_path(instance, filename):
    return os.path.join(connection.schema_name, filename)


class Brand(TimeStamp):
    title = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from="title")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class Products(TimeStamp):
    STAND_ALONE_PRODUCT = 'stand_alone_product'
    PARENT_PRODUCT = 'parent_product'
    PRODUCT_TYPES = ((STAND_ALONE_PRODUCT, "Stand Alone Product"),
                     (PARENT_PRODUCT, "Parent Product"))

    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to=get_upload_path, null=True)
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL, related_name="brand_products")
    public_schema_product_id = models.IntegerField(default=False, db_index=True)
    product_type = models.CharField(max_length=30, choices=PRODUCT_TYPES, default=STAND_ALONE_PRODUCT)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        elif self.url:
            return self.url
        else:
            return ""

    def exists_in_basket(self, basket_id):
        from basket.models import BasketLine
        return BasketLine.objects.filter(product=self, basket_id=basket_id).exists()


    @property
    def imported(self):
        with schema_context(connection.schema_name):
            return Products.objects.filter(public_schema_product_id=self.id).exists()


class ProductVariant(TimeStamp):
    length = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    name = models.CharField(max_length=300)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, related_name="product_product_variants")
    stock = models.PositiveIntegerField(verbose_name="Stock available", default=0)
    price = models.IntegerField()
    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

class ProductImage(TimeStamp):
    image = models.ImageField(upload_to=get_upload_path, null=True)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="variant_product_image")

    def __str__(self):
        return self.variant.name


    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

