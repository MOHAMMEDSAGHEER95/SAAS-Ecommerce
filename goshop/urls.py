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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from onboarding.views import PlanListView, OnboardingFormView, CreateOnboarding, SearchView


schema_view = get_schema_view(
    openapi.Info(
        title="Shopping API",
        default_version="v2",
        description="This Document has all the API endpoints for building setyour shop web pages.",
        terms_of_service="https://www.setyour.shop",
        contact=openapi.Contact(email="mohammed.sagheer95@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', SearchView.as_view(), name='search'),

    path('', PlanListView.as_view(), name='plans'),
    path("customer/", include('customers.urls')),
    path('products/', include('products.urls')),
    path('basket/', include('basket.urls')),
    path('onboarding/', include('onboarding.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include('restapis.urls')),
path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    path('blogs/', include('cms.urls')),
    path('djrichtextfield/', include('djrichtextfield.urls'))

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

