from django.urls import path

from .views import GetNews

app_name = "news"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('get_news/', GetNews.as_view()),
]