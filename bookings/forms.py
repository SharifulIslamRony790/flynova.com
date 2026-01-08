from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    card_number = forms.CharField(max_length=19, required=False, widget=forms.TextInput(attrs={'placeholder': 'XXXX-XXXX-XXXX-XXXX'}))
    card_expiry = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    card_cvc = forms.CharField(max_length=3, required=False, widget=forms.TextInput(attrs={'placeholder': '123'}))
    
    mobile_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': '01XXXXXXXXX'}))
    
    class Meta:
        model = Payment
        fields = ['payment_method', 'transaction_id']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select', 'id': 'id_payment_method'}),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Enter Transaction ID'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('payment_method')

        if method in ['VISA', 'MASTERCARD']:
            if not cleaned_data.get('card_number'):
                self.add_error('card_number', 'Card number is required.')
            if not cleaned_data.get('card_expiry'):
                self.add_error('card_expiry', 'Expiry date is required.')
            if not cleaned_data.get('card_cvc'):
                self.add_error('card_cvc', 'CVC is required.')
        
        elif method in ['BKASH', 'NAGAD']:
            if not cleaned_data.get('mobile_number'):
                self.add_error('mobile_number', 'Mobile number is required.')
            if not cleaned_data.get('transaction_id'):
                self.add_error('transaction_id', 'Transaction ID is required.')

        return cleaned_data
