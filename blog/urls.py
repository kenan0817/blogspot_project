from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('create/',views.article_create_view,name='article_create'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
    path('tag/<slug:tag_slug>/', views.tag_filter, name='tag_filter'),
    path('category/<slug:cat_slug>/', views.category_filter, name='category_filter'),
]
