import pytest
from django.contrib.auth import get_user_model
from django.db import connection, IntegrityError
from django.test import TestCase
from django.utils.text import slugify
from django_tenants.utils import schema_context

from basket.models import Basket
from customers.models import Client
from orders.models import ShippingAddress, Order


@pytest.mark.django_db
class TestShipping(TestCase):

    def test_shipping_creation(self):
        client_data = {'schema_name': 'alice', 'domain_url': 'alice.localhost'}
        client = Client.objects.create(**client_data)
        user_data = {
            "email": "mohammedsagheer75@gmail.com",
            "username": "mohammedsagheer75@gmail.com",
            "password": "qwertyuiop",
            "first_name": "alpha",
            "last_name": "beta"
        }
        with schema_context('alice'):
            user = get_user_model().objects.create(**user_data)
            data = {
                "line_1": "15 oxman lane",
                "line_2": "greenleys",
                "city": "tok_visa",
                "postcode": "MK12 6LG",
                "user_id": user.id
            }
            shipping = ShippingAddress.objects.create(**data)
            assert shipping.line_1 == "15 oxman lane"
            with self.assertRaises(IntegrityError):
                shipping = ShippingAddress.objects.create(**data)

    def test_order_creation(self):
        client_data = {'schema_name': 'alice', 'domain_url': 'alice.localhost'}
        user_data = {
            "email": "mohammedsagheer75@gmail.com",
            "username": "mohammedsagheer75@gmail.com",
            "password": "qwertyuiop",
            "first_name": "alpha",
            "last_name": "beta"
        }
        client = Client.objects.create(**client_data)
        with schema_context('alice'):
            user = get_user_model().objects.create(**user_data)
            basket = Basket.get_basket(user)

            order = Order.objects.create(user=user, basket=basket, number='111111', total_incl_tax=100)
            assert order.number == '111111'
            with self.assertRaises(IntegrityError):
                Order.objects.create(user=user, basket=basket, number='111111', total_incl_tax=100)




