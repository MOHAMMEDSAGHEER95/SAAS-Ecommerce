from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from dashboard.forms import DashboardAdminForm


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


