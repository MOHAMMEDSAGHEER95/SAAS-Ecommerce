from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from onboarding.models import Plan


class PlanListView(TemplateView):

    template_name = 'onboarding/plans.html'

    def get_context_data(self, **kwargs):
        plans = Plan.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        context['plans'] = plans
        return context


