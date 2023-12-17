"""goshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from onboarding.views import PlanListView, OnboardingFormView, CreateOnboarding

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PlanListView.as_view(), name='plans'),
    path('plans/', PlanListView.as_view(), name='plans'),
    path('onboarding/success/<slug:slug>/', CreateOnboarding.as_view(), name="create-onboarding"),
    path('onboarding/success/', TemplateView.as_view(template_name='onboarding/success.html'), name='onboarding-success'),
    path('onboarding/<slug:slug>/', OnboardingFormView.as_view(), name='onboarding'),
    path('products/', include('products.urls')),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

