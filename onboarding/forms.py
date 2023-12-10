from django import forms

from customers.models import Client


class OnboardingForm(forms.ModelForm):
    schema_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    contact_number = forms.CharField(max_length=15)

    class Meta:
        model = Client
        fields = ('schema_name', 'email', 'contact_number')
