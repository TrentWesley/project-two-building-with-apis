from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.views.generic import ListView

from .forms import LoginForm, SignUpForm
from .models import SavedBook


def home(request):
    """Public home page."""
    return render(request, "home.html")


def signup(request):
    """Create an account with Django's built-in form, then log the new user in."""
    if request.user.is_authenticated:
        return redirect("books:list")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, f"Welcome, {user.username}! Your account was created."
            )
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


class StyledLoginView(LoginView):
    """Django's built-in login, with Bootstrap styling.

    Logged-in users are sent to their reading list instead of seeing the form.
    After logging in, users go to a safe "next" URL, otherwise to LOGIN_REDIRECT_URL.
    """

    form_class = LoginForm
    redirect_authenticated_user = True


class LogoutWithMessageView(LogoutView):
    """Django's built-in logout (POST only), plus a confirmation message."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.info(request, "You have been logged out.")
        return response


class BookListView(LoginRequiredMixin, ListView):
    """My Reading List: only the logged-in user's saved books, newest first."""

    template_name = "books/book_list.html"
    context_object_name = "books"

    def get_queryset(self):
        return SavedBook.objects.filter(user=self.request.user).order_by("-created_at")
