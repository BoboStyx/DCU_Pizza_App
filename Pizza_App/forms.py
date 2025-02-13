from django import forms
from .models import Pizza, Topping, Address, Payment_Model

class PizzaForms(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['size', 'crust', 'topping', 'sauce', 'cheese']

    topping = forms.ModelMultipleChoiceField(queryset = Topping.objects.all(), widget = forms.CheckboxSelectMultiple, required = False)


class PaymentForms(forms.ModelForm):
    class Meta:
        model = Payment_Model
        fields = ['name_of_card_owner', 'card_number', 'cvv', 'expiry_month', 'expiry_year']
        widgets = {
            'card_number': forms.TextInput(attrs={'pattern': '[0-9]{16}', 'title': '13-16 digits required'}),
            'expiry_month': forms.TextInput(attrs={'pattern': '[0-9]{2}', 'title': '2 digits required in MM format'}),
            'expiry_year': forms.TextInput(attrs={'pattern': '[0-9]{4}', 'title': '4 digits required in YYYY format'}),
            'cvv': forms.TextInput(attrs={'pattern': '[0-9]{3}', 'title': '3 digits required'})
        }

        labels = {
            'name_of_card_owner': 'Name of Card Owner',
            'card_number': 'Card Number',
            'expiry_month': 'Expiry Month',
            'expiry_year': 'Expiry Year',
            'cvv': 'CVV',
        }
class AddressForms(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'first_address', 'second_address', 'town', 'eircode']