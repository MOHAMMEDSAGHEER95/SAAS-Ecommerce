from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from tenant_schemas.models import TenantMixin

from customers.abstract_model import TimeStamp


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    email = models.EmailField(null=True)
    contact_number = models.CharField(null=True, max_length=15)
    on_trials = models.BooleanField(default=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return f"{self.schema_name}-{self.domain_url}"



class ShippingAddress(TimeStamp):
    line_1 = models.CharField(max_length=250)
    line_2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.line_1}-{self.user.get_full_name()}"

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

