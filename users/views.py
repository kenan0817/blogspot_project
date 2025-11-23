from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .forms import RegisterForm,LoginForm
from django.contrib.auth import logout

def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            # Şifrələrin uyğunluğu
            if password != password_confirm:
                messages.error(request, "Şifrələr uyğun gəlmir!")
                return render(request, 'users/register.html', {"form": form})

            # Username mövcuddur?
            if User.objects.filter(username=username).exists():
                messages.error(request, "Bu istifadəçi adı artıq mövcuddur!")
                return render(request, 'users/register.html', {"form": form})

            # Email mövcuddur?
            if User.objects.filter(email=email).exists():
                messages.error(request, "Bu email artıq istifadə olunur!")
                return render(request, 'users/register.html', {"form": form})


            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )


            login(request, user)

            messages.success(request, "Qeydiyyat uğurla tamamlandı. Xoş gəldin!")
            
            return render(request, 'users/register.html', {
                "form": RegisterForm()  
            })

    return render(request, 'users/register.html', {"form": form})

def login_view(request):
    form=LoginForm(request.POST or None)
    
    if request.method=="POST":
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            
            user=authenticate(request,email=email,password=password)
            
            if user is None:
                messages.error(request,"Istifadeci email-i ve ya sifre yanlisdir!")
                return render(request,'users/login.html',{'form':form})
            
            login(request,user)
            messages.success(request,'Xos geldiniz!')
            
            return redirect('info:home')
    return render(request,'users/login.html',{'form':form})

def logout_view(request):
    logout(request)
    messages.info(request,"Hesabdan cixis edildi")
    return redirect('info:home')