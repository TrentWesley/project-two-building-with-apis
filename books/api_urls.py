"""URLs for the reading list API, included under /api/ in config/urls.py."""

from django.urls import path

from . import api

app_name = "api"

urlpatterns = [
    path("books/", api.BookListAPIView.as_view(), name="book-list"),
    path("books/<int:pk>/", api.BookDetailAPIView.as_view(), name="book-detail"),
]
