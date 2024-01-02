from django.urls import path

from dashboard.views import DashboardHomeView, DashboardLogin, OrderListView, PublicSchemaProductImport, \
    StoreProductListView, OrderEditView, ChangeProductStatus, CreateProductView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard_home'),
    path('login/', DashboardLogin.as_view(), name='dashboard_login'),
    path('orders/', OrderListView.as_view(), name='dashboard_orders'),
    path('orders/<int:pk>/edit/', OrderEditView.as_view(), name='dashboard_orders_edit'),
    path('import-products/', PublicSchemaProductImport.as_view(), name='import_products'),
    path('store-products/', StoreProductListView.as_view(), name='store_products'),
    path('change-product-status/', ChangeProductStatus.as_view(), name='change_product_status'),
    path('create-product/', CreateProductView.as_view(), name='create_product'),
]
