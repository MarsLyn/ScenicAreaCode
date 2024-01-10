from django import forms

from .models import Concern, GiftRelationship

TEXTINPUTCLASS = 'form-control'

class ConcernForm(forms.ModelForm):
    class Meta:
        model = Concern
        fields = ('passive_by',)
        widgets = {
            'passive_by': forms.TextInput(attrs={'class': TEXTINPUTCLASS, 'type': 'hidden'}),
        }

class GiftRelationshipForm(forms.ModelForm):
    class Meta:
        model = GiftRelationship
        fields = ('address', 'receive_user', 'status')
        widgets = {
            'address': forms.TextInput(attrs={'class': TEXTINPUTCLASS}),
            'receive_user': forms.Select(attrs={'class': 'form-select'}),
        }

    # def clean_receive_user(self):
    #     receiveuser = self.cleaned_data.get('receive_user')
    #     if not receiveuser:
    #         raise forms.ValidationError('没有提供有效的接收人')
    #     return receiveuser
    
    # def clean_address(self, *args, **kwargs):
    #     address = self.cleaned_data.get('address')
    #     if 'a' in address:
    #         raise forms.ValidationError('没有提供有效的接收人')
    #     return address