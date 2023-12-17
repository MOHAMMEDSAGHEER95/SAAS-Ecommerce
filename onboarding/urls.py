from django.urls import path
from django.views.generic import TemplateView

from onboarding.views import CreateOnboarding, OnboardingFormView

urlpatterns = [
    path('success/<slug:slug>/', CreateOnboarding.as_view(), name="create-onboarding"),
    path('<slug:slug>/', OnboardingFormView.as_view(), name='onboarding'),
]