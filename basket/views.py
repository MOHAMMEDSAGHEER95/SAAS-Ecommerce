import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, TemplateView
from tenant_schemas.utils import schema_context

from basket.models import Basket
from onboarding.models import Onboarding


# Create your views here.


class AddToBasket(View):

    def post(self, request):
        data = request.POST
        basket = Basket.objects.get(id=request.basket)
        lines = basket.create_basket_lines(data.get('id'), data.get('quantity'))
        return JsonResponse({"message": "Added to Cart", "count": lines})


class BasketDetailView(DetailView):
    model = Basket
    template_name = 'basket/basket.html'

    def get_object(self, queryset=None):
        return Basket.objects.get(id=self.request.basket)


def stripe_basket_checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    line_items = []
    basket = Basket.objects.get(id=request.basket)
    for line in  basket.lines.all():
        price_data = {"product_data": {"name": line.product.title}, "currency": "gbp", "unit_amount": line.product.price * 100}
        line_object = {"price_data": price_data, "quantity": line.quantity}
        line_items.append(line_object)
    stripe_account = ''
    schema_name = request.tenant.schema_name
    with schema_context('public'):
        stripe_account = Onboarding.objects.get(schema_name=schema_name).stripe_connect_id
    success_url = f"http://{request.tenant.domain_url}/basket/payment-success/"
    session = stripe.checkout.Session.create(line_items=line_items,mode="payment",
                                             success_url=success_url + "{CHECKOUT_SESSION_ID}/",
                                             cancel_url="http://localhost:8000/cancel",
                                             stripe_account=stripe_account
                                             )
    basket.status = basket.SUBMITTED
    basket.save()
    request.session.pop('basket')
    return HttpResponseRedirect(session.url)


class SuccessView(TemplateView):
    template_name = 'basket/success.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.retrieve(id=kwargs.get('slug'))
            if session.status == "complete":
                context['status'] = "Success"
        except Exception as e:
            context['status'] = "Error"
        return context




