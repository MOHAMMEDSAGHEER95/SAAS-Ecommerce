from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from tenant_schemas.models import TenantMixin
from tenant_schemas.utils import schema_context

from customers.abstract_model import TimeStamp


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return f"{self.schema_name}-{self.domain_url}"

    def is_basic_plan(self):
        with schema_context('public'):
            return self.client_onboarding.filter(plan__slug='basic').exists()

    def is_enterprise_plan(self):
        with schema_context('public'):
            return self.client_onboarding.filter(plan__slug='enterprise').exists()

    def is_premium_plan(self):
        with schema_context('public'):
            return self.client_onboarding.filter(plan__slug='premium').exists()

    def has_active_plan(self):
        with schema_context('public'):
            return self.client_onboarding.filter(is_active=True).exists()

    def can_publish_cms(self):
        with schema_context('public'):
            return self.is_premium_plan() or self.is_enterprise_plan()

