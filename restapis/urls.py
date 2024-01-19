from django.urls import path

from restapis.views import BasketDetailAPIView, LoginTokenAPIView, AddProductAPI, ProductListView, AddShippingAPI, \
    GetUserShippingAPI, CreateOrderAPI, GetUserOrdersAPI, RegisterView

app_name = 'restapis'

urlpatterns = [
    path('login/', LoginTokenAPIView.as_view(), name='login_api'),
    path('register/', RegisterView.as_view(), name='register_api'),
    path('basket/', BasketDetailAPIView.as_view(), name='basket_detail_api'),
    path('products/', ProductListView.as_view(), name='products_api'),

    path('add-product/', AddProductAPI.as_view(), name='add_product_api'),
    path('add-shipping/', AddShippingAPI.as_view(), name='add_shipping_api'),
    path('get-shipping-address/', GetUserShippingAPI.as_view(), name='get_shipping_api'),
    path('create-order/', CreateOrderAPI.as_view(), name='create_order'),
    path('my-orders/', GetUserOrdersAPI.as_view(), name='my_orders'),
]