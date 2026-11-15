from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path("", views.BookListView.as_view(), name="list"),
    path("save/", views.save_book, name="save"),
    path("<int:pk>/edit/", views.EditBookView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.DeleteBookView.as_view(), name="delete"),
]
