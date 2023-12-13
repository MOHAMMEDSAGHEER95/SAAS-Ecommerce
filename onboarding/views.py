import stripe
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from tenant_schemas.utils import schema_context

from customers.models import Client
from onboarding.forms import OnboardingForm
from onboarding.godaddy.client import GoDaddyClientHelper
from onboarding.models import Plan, Onboarding
from products.models import Products


class PlanListView(TemplateView):

    template_name = 'onboarding/plans.html'
    tenant_homepage = 'onboarding/tenant_home.html'

    def get_context_data(self, **kwargs):
        plans = Plan.objects.filter(is_active=True).order_by('id')
        context = super().get_context_data(**kwargs)
        context['plans'] = plans
        context['tenant'] = connection.schema_name
        return context

    def get_template_names(self):
        if connection.schema_name == 'public':
            return self.template_name
        return self.tenant_homepage


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

            Client.objects.create(domain_url=onboarding.domain_url, schema_name=onboarding.schema_name)
            onboarding.is_active = True
            onboarding.save()
        context = super().get_context_data()
        context['website_url'] = onboarding.domain_url
        context['products'] = Products.objects.filter(is_available=True)
        return context




