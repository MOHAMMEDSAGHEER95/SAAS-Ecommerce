from django.urls import path
from django.views.generic import TemplateView

from basket.views import AddToBasket, BasketDetailView, stripe_basket_checkout, SuccessView

app_name = 'basket'

urlpatterns = [
    path('add-to-basket', AddToBasket.as_view(), name="add_to_basket"),
    path('view-basket', BasketDetailView.as_view(), name="view_basket"),
    path('checkout-basket', stripe_basket_checkout, name="checkout_basket"),
    path('payment-error', TemplateView.as_view(template_name='basket/payment-error.html'), name="payment_error"),
    path('payment-success/<slug:slug>/', SuccessView.as_view(), name="payment_success"),
]