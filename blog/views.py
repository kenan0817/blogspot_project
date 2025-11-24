from django.shortcuts import render,get_object_or_404
from django.shortcuts import render,redirect
from .models import Article,Tag,Category
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.
def blog_list(request):
    
    articles=Article.objects.filter(is_published=True).order_by('-created_at')
    
    paginator=Paginator(articles,4)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    tags=Tag.objects.all()
    categories=Category.objects.all()
    
    context = {
        "page_obj":page_obj,
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
    
    
    paginator=Paginator(articles,4)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    return render(request,'blog/tag_list.html',{'tag':tag,'page_obj':page_obj,'articles':articles,'categories':categories})


def category_filter(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    articles = Article.objects.filter(is_published=True, category=category).order_by('-created_at')
    paginator=Paginator(articles,4)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    
    return render(request, 'blog/tag_list.html',{
        'category': category,
        'page_obj':page_obj,
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


@login_required
def article_update_view(request, slug):
    article = get_object_or_404(Article, slug=slug)

    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('blog:article_detail', slug=article.slug)

    return render(request, 'blog/article_edit.html', {"form": form, "article": article})


def article_delete_view(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.user != article.author:
        messages.error(request, "Bu məqaləni silmək üçün icazəniz yoxdur!")
        return redirect(article.get_absolute_url())

    article.delete()
    messages.success(request, "Məqalə uğurla silindi.")
    return redirect('blog:blog_list')