from django.urls import path

from restapis.views import BasketDetailAPIView, LoginTokenAPIView, AddProductAPI, ProductListView

app_name = 'restapis'

urlpatterns = [
    path('login/', LoginTokenAPIView.as_view(), name='login_api'),
    path('basket/', BasketDetailAPIView.as_view(), name='basket_detail_api'),
    path('products/', ProductListView.as_view(), name='products_api'),

    path('add-product/', AddProductAPI.as_view(), name='add_product_api'),
]