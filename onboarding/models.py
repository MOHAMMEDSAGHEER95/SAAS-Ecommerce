from django.db import models

# Create your models here.
from customers.abstract_model import TimeStamp


class Plan(TimeStamp):
    title = models.CharField(max_length=255)
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
        return self.description.split("*")


class Onboarding(TimeStamp):
    schema_name = models.CharField(max_length=255)
    domain_url = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    plan = models.ForeignKey(Plan, null=True, related_name="onboarding_plan", on_delete=models.CASCADE)
    session_id = models.CharField(max_length=500, null=True, blank=True)
    stripe_connect_id = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Onboarding"
        verbose_name_plural = "Onboardings"

    def __str__(self):
        return self.schema_name

