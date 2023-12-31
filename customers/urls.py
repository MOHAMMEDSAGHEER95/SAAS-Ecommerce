from django.contrib.auth.views import LogoutView
from django.urls import path

from customers.views import CustomerLogin, RegisterCustomer, AddAddress

app_name = "customers"

urlpatterns = [
    path('login/', CustomerLogin.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterCustomer.as_view(), name="register"),
    path('add-address/', AddAddress.as_view(), name="add_address"),
]