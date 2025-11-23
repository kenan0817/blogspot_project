from django.shortcuts import render,get_object_or_404
from django.shortcuts import render,redirect
from .models import Article,Tag,Category
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from django.contrib import messages
# Create your views here.
def blog_list(request):
    
    articles=Article.objects.filter(is_published=True).order_by('-created_at')
    tags=Tag.objects.all()
    categories=Category.objects.all()
    
    context = {
        "articles":articles,
        "tags":tags,
        "categories":categories
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
    categories=Category.objects.all()
    articles=Article.objects.filter(is_published=True,tags=tag).order_by('-created_at')
    return render(request,'blog/tag_list.html',{'tag':tag,'articles':articles,'categories':categories})


def category_filter(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    articles = Article.objects.filter(is_published=True, category=category).order_by('-created_at')
    return render(request, 'blog/tag_list.html', {
        'category': category,
        'articles': articles,
        'tags': Tag.objects.all(),
        'categories': Category.objects.all(),
    })
    

@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()

            messages.success(request, "Məqalə uğurla yaradıldı.")
            return redirect("blog:blog_list")


        return render(request, "blog/article_create.html", {"form": form})


    return render(request, "blog/article_create.html", {"form": form})