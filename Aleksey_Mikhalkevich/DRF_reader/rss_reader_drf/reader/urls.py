from django.urls import path

from .views import GetNewsView, FeedListView, FeedDetailView

app_name = "news"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('get_news/', GetNewsView.as_view()),
    path('feeds/', FeedListView.as_view()),
    path('feeds/<int:pk>', FeedDetailView.as_view()),
]