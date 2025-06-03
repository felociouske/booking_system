from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['transaction_code', 'amount']
        labels = {'transaction_code': 'Enter the M-Pesa Transaction Code','amount': 'Amount Paid (KES)',}
        widgets ={
            'transaction_code': forms.TextInput(attrs={'placeholder': 'e.g. TXHAHUAIJS','class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'placeholder': '6500.00','class': 'form-control'}),
        }