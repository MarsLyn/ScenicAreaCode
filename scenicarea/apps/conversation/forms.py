from django import forms

from .models import ConversationMessage


TEXTINPUTCLASS = 'form-control'

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': TEXTINPUTCLASS, 'rows':1}),
        }