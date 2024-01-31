from django.urls import path

from dashboard.views import DashboardHomeView, DashboardLogin, OrderListView, PublicSchemaProductImport, \
    StoreProductListView, OrderEditView, ChangeProductStatus, CreateProductView, BrandsListView, AddBrandView, \
    EditBrandView, CategoryListView, AddCategoryView, EditCategoryView, EditProductView, BlogsListView, AddBlogsView, \
    EditBlog, OnboardingListView, OnboardingEditView, ChangeStatus, DeleteBrand, DeleteCategory

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
    path('edit-product/<int:pk>/', EditProductView.as_view(), name='edit_product'),
    path('brands/', BrandsListView.as_view(), name='brands_list_view'),
    path('create-brand/', AddBrandView.as_view(), name='create_brand'),
    path('edit-brand/<int:pk>/', EditBrandView.as_view(), name='edit_brand'),
    path('categories/', CategoryListView.as_view(), name='categories_list_view'),
    path('create-category/', AddCategoryView.as_view(), name='create_category'),
    path('edit-category/<int:pk>/', EditCategoryView.as_view(), name='edit_category'),
    path('blogs/', BlogsListView.as_view(), name='blogs_list_view'),
    path('create-blogs/', AddBlogsView.as_view(), name='create_blogs'),
    path('edit-blog/<int:pk>/', EditBlog.as_view(), name='edit_blog'),
    path('change-status/', ChangeStatus.as_view(), name='change_status'),

    path('onboardings/', OnboardingListView.as_view(), name='onboarding_list_view'),
    path('edit-onboardings/<int:pk>/', OnboardingEditView.as_view(), name='onboarding_edit_view'),
    path('delete-brand/<int:pk>/', DeleteBrand.as_view(), name='delete_brand'),
    path('delete-category/<int:pk>/', DeleteCategory.as_view(), name='delete_category'),
]
