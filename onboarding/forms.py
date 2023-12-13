from django import forms

from customers.models import Client
from onboarding.models import Onboarding


class OnboardingForm(forms.ModelForm):
    schema_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    contact_number = forms.CharField(max_length=15)

    class Meta:
        model = Onboarding
        fields = ('schema_name', 'email', 'contact_number', 'first_name', 'last_name')
