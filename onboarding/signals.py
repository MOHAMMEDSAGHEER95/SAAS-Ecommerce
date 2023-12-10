from tenant_schemas.signals import post_schema_sync
from tenant_schemas.models import TenantMixin


def foo_bar(sender, tenant, **kwargs):
    print("hello.....................hello.....................hello.....................")


post_schema_sync.connect(foo_bar, sender=TenantMixin)
