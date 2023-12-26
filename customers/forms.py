from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise ValidationError("Cannot use this email.")
        return email

    def clean(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get("password2")
        if password != password1:
            self.add_error("password", "Passwords are not same.")
        return self.cleaned_data