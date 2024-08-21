from django import forms
from .models import *
from taggit.forms import TagWidget

class AdForm(forms.ModelForm):
    show_contact_info = forms.BooleanField(
        required=False,
        initial=False,
        label='Show contact information',
        help_text='Check this box to make your contact information visible to others.'
    )

    class Meta:
        model = Ad
        fields = ['category', 'title', 'description', 'location', 'postal_code', 'contact_email', 'contact_phone', 'show_contact_info', 'price', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'show_contact_info': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tags': TagWidget(attrs={'class': 'form-control'}),
        }

class AdImageForm(forms.ModelForm):
    class Meta:
        model = AdImage
        fields = ['image']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

