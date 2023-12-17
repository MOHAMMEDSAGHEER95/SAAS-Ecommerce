from django.dispatch import receiver
from tenant_schemas.signals import post_schema_sync
from tenant_schemas.models import TenantMixin


@receiver(post_schema_sync)
def post_schema_sync_handler(sender, tenant, **kwargs):
    # Your additional functionality here
    print(f"Signal received for tenant: {tenant}")



