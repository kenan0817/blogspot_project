from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_published")
    search_fields = ("title", "description", "content")
    list_filter = ("is_published", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at",)
