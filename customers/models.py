from django.db import models

# Create your models here.
from tenant_schemas.models import TenantMixin


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    email = models.EmailField(null=True)
    contact_number = models.CharField(null=True, max_length=15)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return f"{self.schema_name}-{self.domain_url}"
