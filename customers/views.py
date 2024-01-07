from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView

from customers.forms import RegisterUserForm, AddAddressForm


# Create your views here.

class CustomerLogin(FormView):
    # TODO: remove the html code and replace with scratch code
    form_class = AuthenticationForm
    template_name = 'customers/login.html'
    success_url = '/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class RegisterCustomer(FormView):
    form_class = RegisterUserForm
    template_name = 'customers/register.html'
    success_url = '/customer/login'


    def form_valid(self, form):
        form.cleaned_data.pop("password2")
        user = form.save()
        user.username = form.cleaned_data['email']
        user.set_password(form.cleaned_data.pop("password"))
        user.save()
        return super().form_valid(form)


class AddAddress(FormView):
    form_class = AddAddressForm


    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            address = form.save()
            address.user = request.user
            address.save()
            return JsonResponse({"message": "address added"}, status=200)
        return JsonResponse({"errors": form.errors})


