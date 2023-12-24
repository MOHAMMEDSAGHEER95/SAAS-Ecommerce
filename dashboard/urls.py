from django.urls import path

from dashboard.views import DashboardHomeView, DashboardLogin

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard_home'),
    path('login/', DashboardLogin.as_view(), name='dashboard_login')
]