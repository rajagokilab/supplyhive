from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'p-2 rounded-lg border border-gray-400', 'placeholder': 'Enter your Name'}),
            'email': forms.EmailInput(attrs={'class': 'p-2 rounded-lg border border-gray-400', 'placeholder': 'Enter Email ID'}),
            'phone': forms.TextInput(attrs={'class': 'p-2 rounded-lg border border-gray-400', 'placeholder': 'Enter your number'}),
            'message': forms.TextInput(attrs={'class': 'p-2 rounded-lg border border-gray-400', 'placeholder': 'Enter Message'}),
        }
