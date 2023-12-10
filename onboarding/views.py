from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from onboarding.forms import OnboardingForm
from onboarding.models import Plan


class PlanListView(TemplateView):

    template_name = 'onboarding/plans.html'

    def get_context_data(self, **kwargs):
        plans = Plan.objects.filter(is_active=True).order_by('id')
        context = super().get_context_data(**kwargs)
        context['plans'] = plans
        return context


class OnboardingFormView(FormView):
    template_name = 'onboarding/onboarding_form.html'
    form_class = OnboardingForm

    def form_valid(self, form):
        clientobj = form.save(commit=False)
        clientobj.domain_url = clientobj.schema_name + '.localhost'
        clientobj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('plans')




