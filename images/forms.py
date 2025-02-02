from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full mt-2 px-4 py-2'}),
            'email': forms.EmailInput(attrs={'class': 'w-full mt-2 px-4 py-2'}),
            'message': forms.Textarea(attrs={'class': 'w-full mt-2 px-4 py-2'}),
        }
