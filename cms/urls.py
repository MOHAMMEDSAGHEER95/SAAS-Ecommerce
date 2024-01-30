from django.urls import path

from cms.views import BlogListView, BlogDetailView

app_name = 'basket'

urlpatterns = [
path('', BlogListView.as_view(), name='blog_list'),
path('<int:pk>/', BlogDetailView.as_view(), name='blog_details'),
]