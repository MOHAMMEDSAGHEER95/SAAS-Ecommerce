from django.urls import path

from basket.views import AddToBasket, BasketDetailView

app_name = 'basket'

urlpatterns = [
    path('add-to-basket', AddToBasket.as_view(), name="add_to_basket"),
    path('view-basket', BasketDetailView.as_view(), name="view_basket"),
]