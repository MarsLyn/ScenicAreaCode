from django import forms

from .models import Wallet

TEXTINPUTCLASS = 'form-control form-control-lg'

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ('balance',)
        widgets = {
            'balance': forms.NumberInput(attrs={'class': TEXTINPUTCLASS, 'placeholder':'输入你的充值金额'})
        }

    def clean_balance(self):
        balance = self.cleaned_data.get('balance')
        print(balance)
        if balance <= 0:
            raise forms.ValidationError('充值金额不能小于0')
        else:
            return balance