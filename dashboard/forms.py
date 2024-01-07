from django import forms

from products.models import Products, Brand


class DashboardAdminForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())


class AddStoreProduct(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('title', 'description', 'price', 'brand', 'product_type', 'image')


class AddBrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = ('title',)


    def clean_title(self):
        return self.cleaned_data['title'].capitalize()