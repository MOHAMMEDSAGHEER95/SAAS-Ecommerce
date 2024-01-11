import time

import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import connection, IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView, FormView, ListView
from elasticsearch_dsl import Q
from tenant_schemas.utils import schema_context

from basket.models import BasketLine
from customers.models import Client
from onboarding.forms import OnboardingForm
from onboarding.godaddy.client import GoDaddyClientHelper
from onboarding.models import Plan, Onboarding
from products.documents import ProductDocument
from products.models import Products


class PlanListView(ListView):
    model = Products
    template_name = 'onboarding/plans.html'
    tenant_homepage = 'onboarding/tenant_home.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        plans = Plan.objects.filter(is_active=True).order_by('id')
        context = super().get_context_data(**kwargs)
        context['plans'] = plans
        context['tenant'] = connection.schema_name
        if connection.schema_name != 'public':
            with schema_context(connection.schema_name):
                context['basket_lines'] = BasketLine.objects.filter(basket_id=self.request.basket).count()
        return context

    def get_queryset(self):
        if connection.schema_name != 'public':
            return Products.objects.filter(is_available=True)
        return Plan.objects.filter(is_active=True).order_by('id')


    def get_template_names(self):
        if connection.schema_name == 'public':
            return self.template_name
        return self.tenant_homepage


class SearchView(TemplateView):
    template_name = 'onboarding/tenant_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        # response = ProductDocument.search().filter("term", tenant=self.request.tenant.schema_name).filter("term", is_available=True)
        # wildcard_query = Q("wildcard", title={"value": f"*{q.lower()}*"})
        # response = response.query(wildcard_query)
        response = Products.objects.filter(title__icontains=q)
        context['products'] = response
        context['searchterm'] = q
        return context




class OnboardingFormView(FormView):
    template_name = 'onboarding/onboarding_form.html'
    form_class = OnboardingForm
    plan = None

    def form_valid(self, form):
        clientobj = form.save(commit=False)
        clientobj.domain_url = clientobj.schema_name + "." + settings.PUBLIC_DOMAIN_URL
        self.plan = Plan.objects.get(slug=self.kwargs.get('slug'))
        clientobj.plan = self.plan

        stripe.api_key = settings.STRIPE_SECRET_KEY
        if settings.IS_PRODUCTION:
            success_url = f"http://{settings.PUBLIC_DOMAIN_URL}/onboarding/success/"
        else:
            success_url = f"http://localhost:8000/onboarding/success/"
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "product_data": {"name": self.plan.title},
                        "unit_amount": self.plan.price * 100,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=success_url + "{CHECKOUT_SESSION_ID}/",
            cancel_url="http://localhost:8000/cancel",
        )
        clientobj.session_id = session.id
        clientobj.save()
        return redirect(session.url)


class CreateOnboarding(TemplateView):
    template_name = "onboarding/payment_success.html"

    def get_context_data(self, **kwargs):
        onboarding = Onboarding.objects.get(session_id=self.kwargs.get('slug'))
        if onboarding.is_active is False:
            if settings.IS_PRODUCTION:
                godaddy = GoDaddyClientHelper()
                schema_name = onboarding.schema_name
                godaddy.add_cname_to_dns(schema_name)

            Client.objects.create(domain_url=onboarding.domain_url.lower(), schema_name=onboarding.schema_name.lower())
            onboarding.is_active = True
            onboarding.save()
        context = super().get_context_data()
        context['website_url'] = onboarding.domain_url
        context['products'] = Products.objects.filter(is_available=True)
        context['schema_name'] = onboarding.schema_name
        with schema_context(onboarding.schema_name):
            try:
                user = User.objects.create(username='admin')
                user.set_password("qwertyuiop")
                user.is_superuser = True
                user.is_staff = True
                user.save()
                site = Site.objects.first()
                site.domain = onboarding.domain_url
                site.save()
            except IntegrityError as e:
                pass
        return context




