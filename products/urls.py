from django.urls import path

from products.views import AddProductFromPublicSchema


app_name = 'products'

urlpatterns = [
    path('add-product/', AddProductFromPublicSchema.as_view(), name='add_product'),
    # Add more product-related URL patterns as needed
]
