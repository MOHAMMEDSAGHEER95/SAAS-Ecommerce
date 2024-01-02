from django import forms

from products.models import Products


class DashboardAdminForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())


class AddStoreProduct(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('title', 'description', 'price', 'brand', 'product_type', 'image')