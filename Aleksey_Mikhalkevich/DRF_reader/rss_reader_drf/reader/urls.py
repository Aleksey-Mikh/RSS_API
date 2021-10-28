from django.urls import path

from .views import GetNewsView, FeedListView, FeedDetailView, NewsListView, NewsDetailView, DownloadPdfView

app_name = "news"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('download/', DownloadPdfView.as_view(), name="download_pdf"),
    path('get_news/', GetNewsView.as_view()),
    path('feeds/', FeedListView.as_view()),
    path('feeds/<int:pk>', FeedDetailView.as_view()),
    path('news/', NewsListView.as_view()),
    path('news/<int:pk>', NewsDetailView.as_view()),
]
