from django.contrib import admin
from django.urls import include, path

from books import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/login/", views.StyledLoginView.as_view(), name="login"),
    path("accounts/logout/", views.LogoutWithMessageView.as_view(), name="logout"),
    path("search/", views.search, name="search"),
    path("books/", include("books.urls")),
    path("api/", include("books.api_urls")),
    path("admin/", admin.site.urls),
]
