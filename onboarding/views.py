from django.conf import settings
from django.contrib.sites.models import Site
from django.db import connection
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from tenant_schemas.utils import schema_context

from onboarding.forms import OnboardingForm
from onboarding.models import Plan


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

    def form_valid(self, form):
        clientobj = form.save(commit=False)
        clientobj.domain_url = clientobj.schema_name + "." + settings.PUBLIC_DOMAIN_URL
        clientobj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('plans')




