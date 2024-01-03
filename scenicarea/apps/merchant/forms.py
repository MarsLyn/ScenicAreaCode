from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Commodity, AssistantImages

TEXTINPUTCLASS = 'form-control'

class ToppingSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option["attrs"]["data-title"] = value.instance.title
        return option


class GoodAddForm(forms.ModelForm):
    template_name = "merchant/create.html"
    class Meta:
        model = Commodity
        # fields = ['title']
        fields = '__all__'
        exclude = ['create_date', 'update_date', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': TEXTINPUTCLASS}),
            'details': forms.Textarea(attrs={'class': TEXTINPUTCLASS, 'rows': 6}),
            'price': forms.NumberInput(attrs={'class': TEXTINPUTCLASS}),
            'inventory': forms.NumberInput(attrs={'class': TEXTINPUTCLASS}),
            'picture': forms.FileInput(attrs={'class': TEXTINPUTCLASS}),
        }

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        if 'CFE' in title:
            raise forms.ValidationError('包含了CFE关键字')
        return title
    
class AssistantImagesForm(forms.ModelForm):
    class Meta:
        model = AssistantImages
        fields = '__all__'
        exclude = ['create_date', 'update_date', 'commodity']
        widgets = {
            'picture': forms.FileInput(attrs={'class': TEXTINPUTCLASS}),
            # 'commodity': forms.Select(attrs={'class': 'form-select'}),
        }

AsInlineFormSet = modelformset_factory(AssistantImages, form=AssistantImagesForm, extra=2)
    
class GoodChangeForm(GoodAddForm):
    template_name = "merchant/details.html"
        
class SingupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': TEXTINPUTCLASS}),
            'email': forms.EmailInput(attrs={'class': TEXTINPUTCLASS}),
            'password1': forms.PasswordInput(attrs={'class': TEXTINPUTCLASS}),
            'password2': forms.PasswordInput(attrs={'class': TEXTINPUTCLASS}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': TEXTINPUTCLASS}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': TEXTINPUTCLASS}))