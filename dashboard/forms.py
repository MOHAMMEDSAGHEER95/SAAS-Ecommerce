from django import forms
from djrichtextfield.widgets import RichTextWidget

from cms.models import Blog
from products.models import Products, Brand, Category, ProductImage


class DashboardAdminForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())


class AddStoreProduct(forms.ModelForm):
    width = forms.IntegerField(initial=0)
    height = forms.IntegerField(initial=0)
    weight = forms.IntegerField(initial=0)
    length = forms.IntegerField(initial=0)
    stock = forms.IntegerField(initial=10, min_value=10)
    price = forms.IntegerField(min_value=0)

    class Meta:
        model = Products
        fields = ('title', 'description', 'price', 'brand', 'product_type', 'image',
                  'category', 'length', 'width', 'height', 'stock', 'weight', 'length')


class AddBrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = ('title',)

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)


    def clean_title(self):
        return self.cleaned_data['title'].capitalize()


class AddBlogForm(forms.ModelForm):
    body = forms.CharField(widget=RichTextWidget())
    class Meta:
        model = Blog
        fields = ('title', 'body', 'status')