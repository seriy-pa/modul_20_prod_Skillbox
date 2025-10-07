from django.contrib import admin

# Register your models here.
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = "id", "title", "content", "pub_date"