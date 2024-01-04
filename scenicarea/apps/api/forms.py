from django import forms

from .models import Concern

TEXTINPUTCLASS = 'form-control'

class ConcernForm(forms.ModelForm):
    class Meta:
        model = Concern
        fields = ('passive_by',)
        widgets = {
            'passive_by': forms.TextInput(attrs={'class': TEXTINPUTCLASS, 'type': 'hidden'})
        }