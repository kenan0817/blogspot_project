from django.shortcuts import render
from blog.models import Tag,Category
from .forms import ContactForm
# Create your views here.

def home(request):
    context={
        'tags':Tag.objects.all(),
        'categories':Category.objects.all()
    }
    return render(request,'info/index.html',context)


def contact_view(request):
    success = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()          
            success = True      
            form = ContactForm() 
    else:
        form = ContactForm()

    context = {
        'form': form,
        'success': success,
    }
    return render(request, 'info/contact.html', context)

def about_view(request):
    return render(request,'info/about.html')