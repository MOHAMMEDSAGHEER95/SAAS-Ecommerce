from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.utils import timezone
from .models import Basket

class BasketModelTestCase(TestCase):
    def test_basket_creation(self):
        # Create a user (you may need to import User model)
        user = User.objects.create(username="testuser")

        # Create a Basket instance
        basket = Basket.objects.create(user=user, status=Basket.OPEN)

        # Assert that the Basket was created successfully
        self.assertEqual(basket.user, user)
        self.assertEqual(basket.status, Basket.OPEN)
        self.assertIsNone(basket.submitted_at)

    def test_basket_status_choices(self):
        # Check if status choices are correctly defined
        basket = Basket()

        expected_status = ["Open", "Submitted", "Merged"]
        status_choices = [status[0] for status in basket.STATUS]

        self.assertListEqual(status_choices, expected_status)

    def test_basket_submission(self):
        # Create a user (you may need to import User model)
        user = User.objects.create(username="testuser")

        # Create a Basket instance
        basket = Basket.objects.create(user=user, status=Basket.OPEN)

        # Simulate basket submission
        basket.submit()

        # Assert that the basket status is now "Submitted"
        self.assertEqual(basket.status, Basket.SUBMITTED)
        self.assertIsNotNone(basket.submitted_at)

