from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.http import HttpRequest, HttpResponse

from .models import Article


def start_blogapp(request: HttpRequest) -> HttpResponse:
    return render(request, "blogapp/base.html")


class ArticlesListView(ListView):
    queryset = (Article.objects.defer("content")
                .select_related("author", "category")
                .prefetch_related("tags"))

