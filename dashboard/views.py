from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView

from dashboard.forms import DashboardAdminForm
from orders.models import Order
from products.models import Products
from tenant_schemas.utils import schema_context


# Create your views here.


class DashboardHomeView(PermissionRequiredMixin, TemplateView):
    permission_required = 'auth.view_user'
    login_url = '/dashboard/login'
    template_name = 'dashboard/dashboard_home.html'

    def has_permission(self):
        # Check if the user is a superuser
        return self.request.user.is_superuser


class DashboardLogin(FormView):
    template_name = 'dashboard/dashboard_login.html'
    form_class = DashboardAdminForm
    success_url = '/dashboard'


    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid credentials")
            return self.form_invalid(form)


class OrderListView(ListView):
    model = Order
    queryset = Order.objects.all()
    context_object_name = 'orders'
    template_name = 'dashboard/orders.html'

    def get_queryset(self):
        if self.request.GET.get('number'):
            return Order.objects.filter(number__icontains=self.request.GET.get('number'))
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('number'):
            context['query'] = self.request.GET.get('number')
        return context


class PublicSchemaProductImport(TemplateView):
    model = Products
    context_object_name = 'products'
    template_name = 'dashboard/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = []
        with schema_context('public'):
            for i in Products.objects.all():
                product_list.append(i)
            context['items'] = product_list
        return context


class StoreProductListView(ListView):
    queryset = Products.objects.filter(is_available=True)
    context_object_name = 'items'
    template_name = 'dashboard/products.html'






