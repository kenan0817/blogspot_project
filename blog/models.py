from django.db import models
from django.urls import reverse
# Create your models here.
class Article(models.Model):
    title=models.CharField(max_length=150)
    slug=models.SlugField(unique=True)
    description=models.TextField(null=True,blank=True)
    content=models.TextField()
    image=models.ImageField(upload_to="articles/",null=True,blank=True)
    tags=models.ManyToManyField("Tag",blank=True,related_name="articles")
    created_at=models.DateTimeField(auto_now_add=True)
    uptadet_at=models.DateTimeField(auto_now=True)
    is_published=models.BooleanField(default=True)
    view_count=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:article_detail", kwargs={"slug": self.slug})
    

class Tag(models.Model):
    name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    