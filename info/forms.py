from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=['name','email','message']
        widgets={
            'name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Adiniz'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Email unvaniniz'
            }),
            'message':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Mesajiniz',
                'rows':5
            }),
        }
        labels={
            'name': 'Ad',
            'email': 'Email',
            'message': 'Mesaj',
        }
        