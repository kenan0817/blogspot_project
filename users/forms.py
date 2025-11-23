from django import forms
from django.contrib.auth.models import User


from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(
        label="İstifadəçi adı",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={"required": "İstifadəçi adı boş ola bilməz"}
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        error_messages={"required": "Email boş ola bilməz", "invalid": "Email formatı düzgün deyil"}
    )

    password = forms.CharField(
        label="Şifrə",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        error_messages={"required": "Şifrə boş ola bilməz"}
    )

    password_confirm = forms.CharField(
        label="Şifrə təsdiqi",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        error_messages={"required": "Şifrə təsdiqi boş ola bilməz"}
    )


class LoginForm(forms.Form):
    username=forms.CharField(
        label="Istifadeci adi",
        widget=forms.TextInput(attrs={"class":"form-control"}),
        error_messages={"requires":"Istifadeci adi bos ola bilmez"}
    )
    
    password=forms.CharField(
        label="Sifre",
        widget=forms.PasswordInput(attrs={"class":"form-control"}),
        error_messages={"required":"Sifre bos ola bilmez"}
    )