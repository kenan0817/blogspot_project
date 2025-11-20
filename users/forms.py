from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Sifreniz'
        })
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Sifreni tesdiqle'
        })
    )
    class Meta:
        model=User
        fields=['username','email','password']
        
        widgets={
            'username':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Istifadeci adi'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Email unvaniniz'
            }),
        }


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)