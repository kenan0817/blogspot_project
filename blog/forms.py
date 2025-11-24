from django import forms
from .models import Article, Category, Tag

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "description", "content", "image", "category", "tags"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Məqalənin başlığı"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Qısa açıqlama (SEO üçün vacibdir)",
                "rows": 3
            }),

            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Məqalə mətni",
            }),

            "category": forms.Select(attrs={
                "class": "form-control"
            }),

            "tags": forms.SelectMultiple(attrs={
                "class": "form-control"
            }),
        }
