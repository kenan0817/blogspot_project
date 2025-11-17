from django.shortcuts import render
from .models import Article
# Create your views here.
def blog_list(request):
    
    articles=Article.objects.filter(is_published=True).order_by('-created_at')
    
    context = {
        "articles":articles
    }
    return render(request,'blog/blog_list.html',context)