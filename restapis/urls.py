from django.urls import path

from restapis.views import BasketDetailAPIView, LoginTokenAPIView

app_name = 'restapis'

urlpatterns = [
    path('login', LoginTokenAPIView.as_view(), name='login_api'),
    path('basket', BasketDetailAPIView.as_view(), name='basket_detail_api')
]