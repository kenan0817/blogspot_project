from django.shortcuts import render,get_object_or_404
from django.shortcuts import render
from .models import Article
# Create your views here.
def blog_list(request):
    
    articles=Article.objects.filter(is_published=True).order_by('-created_at')
    
    context = {
        "articles":articles
    }
    return render(request,'blog/blog_list.html',context)


def article_detail(request,slug):
    article=get_object_or_404(Article,slug=slug,is_published=True)
    
    context={
        "article":article
    }
    
    return render(request,'blog/blog_detail.html',context)