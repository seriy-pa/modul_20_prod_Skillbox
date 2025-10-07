from django.urls import path

from .views import start_blogapp, ArticlesListView

app_name = "blogapp"

urlpatterns = [
    path("", start_blogapp, name="start_blogapp"),
    path("articles/", ArticlesListView.as_view(), name="articles_list"),
]
