from django.shortcuts import render,get_object_or_404
from django.shortcuts import render
from .models import Article,Tag
# Create your views here.
def blog_list(request):
    
    articles=Article.objects.filter(is_published=True).order_by('-created_at')
    tags=Tag.objects.all()
    
    context = {
        "articles":articles,
        "tags":tags,
    }
    return render(request,'blog/blog_list.html',context)


def article_detail(request,slug):
    article=get_object_or_404(Article,slug=slug,is_published=True)
    article.view_count +=1
    article.save(update_fields=['view_count'])
    context={
        "article":article
    }
    
    return render(request,'blog/blog_detail.html',context)


def tag_filter(request,tag_slug):
    tag=get_object_or_404(Tag,slug=tag_slug)
    articles=Article.objects.filter(is_published=True,tags=tag).order_by('-created_at')
    return render(request,'blog/tag_list.html',{'tag':tag,'articles':articles})