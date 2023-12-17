from django.urls import path

from basket.views import AddToBasket


app_name = 'basket'

urlpatterns = [
    path('add-to-basket', AddToBasket.as_view(), name="add_to_basket")
]