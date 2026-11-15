from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path("", views.BookListView.as_view(), name="list"),
    path("save/", views.save_book, name="save"),
]
