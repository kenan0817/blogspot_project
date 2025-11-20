from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
# Create your views here.

def register_view(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            password_confirm=form.cleaned_data.get('password_confirm')
            # eger istifadecini yazdigi sifreler uygun gelmese istifadeci bu mesaji gorecek
            if password != password_confirm:
                messages.error(request,'Sifreler uygun gelmir!')
                return render(request,'users/register.html',{'form':form})
            
            # eger artiq bu adda istifadeci varsa bu mesaj gelemlidir
            if User.objects.filter(username=username).exists():
                messages.error(request,'Bu istifadeci artiq movcuddur')
                return render(request,'users/register.html',{'form':form})
            
            # eger eyni email-dirse istifadeci bu meaji gorecek
            if User.objects.filter(email=email).exists():
                messages.error(request,"Bu email artiq istifade olunub!")
                return render(request,'users/register.html',{'form':form})
            
            # eger her sey qaydasindadirsa Useri yarat
            user=User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            messages.success(request,"Qeydiyyat ugurla basa catdi.")
            return redirect('users:login')
        else:
            return render(request,'users/register.html',{'form':form})
    else:
        form=RegisterForm()
        return render(request,'users/register.html',{'form':form})

def login_view(request):
    return render(request,'users/login.html')