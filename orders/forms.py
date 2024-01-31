from django import forms

from orders.models import Order


class OrderEdit(forms.ModelForm):
    number = forms.CharField(disabled=True)

    class Meta:
        model = Order
        fields = ('number', 'user', 'status', 'notes', 'transaction_id', 'payment_method', 'total_incl_tax', 'tracking_url')
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
            'total_incl_tax': forms.TextInput(attrs={'class': 'form-control'}),
            'tracking_url': forms.TextInput(attrs={'class': 'form-control'}),
        }