import pytest
from django.db import connection
from django.test import TestCase
from django.utils.text import slugify

from products.documents import ProductDocument
from products.models import Products, Brand, Category


@pytest.mark.django_db
class TestProduct(TestCase):
    def setUp(self):
        # Setup code for each test (e.g., create test data)
        pass

    def test_product_creation(self):
        product = Products.objects.create(title="Test Product",description="Test description", price=10.0)
        assert product.title == "Test Product"
        assert product.price == 10.0

    def test_product_editing(self):
        product = Products.objects.create(title="Initial Product", price=15.0)
        product.title = "Updated new Product"
        product.save()
        updated_product = Products.objects.get(id=product.id)
        assert updated_product.title == "Updated new Product"


    def test_product_elastic(self):
        response = ProductDocument.search().filter("term", tenant='public').filter("term", title="Updated new Product")
        print(response.count())
        assert response.count() > 0

    def test_brand_creation(self):
        brand = Brand.objects.create(title='Puma')
        assert slugify('Puma') == brand.slug

    def test_category_creation(self):
        category = Category.objects.create(title='Electronics')
        assert category.title == 'Electronics'
        assert category.slug == slugify('Electronics')