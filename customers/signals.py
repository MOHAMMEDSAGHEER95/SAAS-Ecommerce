from django.contrib.auth.models import User
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver
from tenant_schemas.signals import post_schema_sync
from tenant_schemas.models import TenantMixin

from customers.email import SendEmail
from customers.models import Client


@receiver(post_schema_sync)
def post_schema_sync_handler(sender, tenant, **kwargs):
    # Your additional functionality here
    print(f"Signal received for tenant: {tenant}")


@receiver(post_save, sender=User)
def send_welcome_email_signal(sender, instance, created, **kwargs):
    if created:
        client = Client.objects.get(schema_name=connection.schema_name)
        SendEmail().send_welcome_email(client.domain_url, instance)




