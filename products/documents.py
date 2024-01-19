# documents.py
from django.db import connection
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry


from products.models import Products


@registry.register_document
class ProductDocument(Document):
    id = fields.IntegerField()
    title = fields.TextField()
    description = fields.TextField()
    tenant = fields.TextField()
    get_image_url = fields.TextField()
    brand = fields.TextField()
    category = fields.TextField()
    class Index:
        # Name of the Elasticsearch index
        name = 'products'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Products
        fields = ['price', 'is_available', 'search_keywords']


    def prepare_tenant(self, instance):
        return connection.schema_name

    def prepare_get_image_url(self, instance):
        return instance.get_image_url

    def prepare_id(self, instance):
        return instance.id

    def prepare_brand(self, instance):
        if instance.brand:
            return instance.brand.title
        return ""

    def prepare_category(self, instance):
        if instance.category:
            return instance.category.title
        return ""

