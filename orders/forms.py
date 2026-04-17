from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem
from products.models import Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Order.STATUS_CHOICES),
        }


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, fields=('product', 'quantity', 'price'), extra=1, can_delete=True
)

