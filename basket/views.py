import stripe
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, TemplateView
from tenant_schemas.utils import schema_context

from basket.models import Basket
from onboarding.models import Onboarding
from orders.models import Order
from products.models import Products


# Create your views here.


class AddToBasket(View):

    def post(self, request):
        data = request.POST
        basket = Basket.objects.get(id=request.basket)
        product_id = data.get('id')
        try:
            product_count = basket.get_product_line_count(product_id)
            if int(data.get('quantity')) > Products.objects.get(id=product_id).stock:
                return JsonResponse({"message": "Cannot add to cart low stock", "product_count": product_count}, status=400)
        except Exception as e:
            print(str(e))
        lines = basket.create_basket_lines(product_id, data.get('quantity'))
        product_count = basket.get_product_line_count(product_id)
        return JsonResponse({"message": "Added to Cart", "count": lines, "product_count": product_count})


class BasketDetailView(DetailView):
    model = Basket
    template_name = 'basket/basket.html'

    def get_object(self, queryset=None):
        return Basket.objects.get(id=self.request.basket)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lines_exists'] = self.get_object().lines.exists()
        if self.request.user.is_authenticated:
            context['addresses'] = self.request.user.shipping_address.all()
        return context



def stripe_basket_checkout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/customer/login?next=/basket/view-basket')
    stripe.api_key = settings.STRIPE_SECRET_KEY
    line_items = []
    request.session["address_id"] = request.POST.get("selected_shipping_address")
    basket = Basket.objects.get(id=request.basket)
    for line in  basket.lines.all():
        price_data = {"product_data": {"name": line.product.title}, "currency": "gbp", "unit_amount": line.product.price * 100}
        line_object = {"price_data": price_data, "quantity": line.quantity}
        line_items.append(line_object)
    stripe_account = ''
    schema_name = request.tenant.schema_name
    with schema_context('public'):
        stripe_account = Onboarding.objects.get(schema_name=schema_name).stripe_connect_id
    success_url = f"https://{request.tenant.domain_url}/basket/payment-success/"
    cancel_url = f"https://{request.tenant.domain_url}/basket/payment-error/"
    session = stripe.checkout.Session.create(line_items=line_items,mode="payment",
                                             success_url=success_url + "{CHECKOUT_SESSION_ID}/",
                                             cancel_url=cancel_url,
                                             stripe_account=stripe_account
                                             )
    return HttpResponseRedirect(session.url)


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'basket/success.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            schema_name = self.request.tenant.schema_name
            with schema_context('public'):
                stripe_account = Onboarding.objects.get(schema_name=schema_name).stripe_connect_id
            session = stripe.checkout.Session.retrieve(id=kwargs.get('slug'), stripe_account=stripe_account)
            order_created = False
            if Order.objects.filter(transaction_id=session.id).exists():
                order = Order.objects.filter(transaction_id=session.id).first()
                context['order'] = order
                order_created = True
                context['status'] = "Success"
            if session.status == "complete" and not order_created:
                context['status'] = "Success"
                basket = Basket.objects.get(id=self.request.basket)
                basket.status = basket.SUBMITTED
                basket.submitted_at = timezone.now()
                basket.save()
                number = settings.ORDER_NUMBERING_FROM + basket.id
                shipping_address = self.request.session.get("address_id")
                order = Order.objects.create(basket=basket, user=basket.user, number=str(number),
                                     total_incl_tax=session.amount_total/100, transaction_id=session.id,
                                     shipping_address_id=shipping_address)
                context['order'] = order
        except Exception as e:
            context['status'] = "Error"
        return context




