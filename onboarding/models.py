from django.db import models

# Create your models here.
from customers.abstract_model import TimeStamp
from customers.models import Client


class Plan(TimeStamp):
    BASIC = 'basic'
    ENTERPRISE = 'enterprise'
    PREMIUM = 'premium'
    plans = ((BASIC, 'Basic'), (ENTERPRISE, 'Enterprise'), (PREMIUM, 'Premium'))
    title = models.CharField(max_length=255, choices=plans)
    description = models.TextField()
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

    def __str__(self):
        return self.title

    def decription_array(self):
        return self.description.split("\n")


class Onboarding(TimeStamp):
    schema_name = models.CharField(max_length=255)
    domain_url = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(null=True)
    plan = models.ForeignKey(Plan, null=True, related_name="onboarding_plan", on_delete=models.CASCADE)
    session_id = models.CharField(max_length=500, null=True, blank=True)
    stripe_connect_id = models.CharField(max_length=500, null=True, blank=True)
    client = models.ForeignKey(Client, null=True, related_name='client_onboarding', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Onboarding"
        verbose_name_plural = "Onboardings"

    def __str__(self):
        return self.schema_name

