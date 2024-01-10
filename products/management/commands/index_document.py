from django.core.management import BaseCommand
from tenant_schemas.utils import schema_context

from customers.models import Client
from products.models import Products


class Command(BaseCommand):

    def handle(self, *args, **options):
        with schema_context('public'):
            for product in Products.objects.all():
                product.save()
        for tenant in Client.objects.all():
            with schema_context(tenant.schema_name):
                for product in Products.objects.all():
                    product.save()
        print("Indexing completed..")
