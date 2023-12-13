from django import forms
from django.core.exceptions import ValidationError

from customers.models import Client
from onboarding.models import Onboarding


class OnboardingForm(forms.ModelForm):
    schema_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    contact_number = forms.CharField(max_length=15)

    class Meta:
        model = Onboarding
        fields = ('schema_name', 'email', 'contact_number', 'first_name', 'last_name')

    def clean_schema_name(self,):
        schema_name = self.cleaned_data['schema_name']
        if Onboarding.objects.filter(schema_name=schema_name).exists():
            raise ValidationError('schema name already taken.')
        return schema_name
