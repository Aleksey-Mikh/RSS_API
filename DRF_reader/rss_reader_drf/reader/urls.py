from django.urls import path

from .views import (
    GetNewsView,
    FeedListView,
    FeedDetailView,
    NewsListView,
    NewsDetailView,
    DownloadPdfView,
    DownloadHTMLView
)

app_name = "news"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('download_pdf/', DownloadPdfView.as_view(), name="download_pdf"),
    path('download_html/', DownloadHTMLView.as_view(), name="download_html"),
    path('get_news/', GetNewsView.as_view(), name="get_news"),
    path('feeds/', FeedListView.as_view(), name="feeds"),
    path('feeds/<int:pk>', FeedDetailView.as_view(), name="feeds_pk"),
    path('news/', NewsListView.as_view(), name="news"),
    path('news/<int:pk>', NewsDetailView.as_view(), name="news_pk"),
]
