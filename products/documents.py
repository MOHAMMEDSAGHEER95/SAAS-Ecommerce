# documents.py
from django.db import connection
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry


from products.models import Products


@registry.register_document
class ProductDocument(Document):
    title = fields.TextField()
    description = fields.TextField()
    tenant = fields.TextField()
    class Index:
        # Name of the Elasticsearch index
        name = 'products'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Products
        fields = ['price']


    def prepare_tenant(self, instance):
        return connection.schema_name

