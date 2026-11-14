import logging

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.views.generic import ListView

from . import openlibrary
from .forms import LoginForm, SignUpForm
from .models import SavedBook

logger = logging.getLogger(__name__)


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


@login_required
def search(request):
    """Search Open Library by title (GET /search/?title=...)."""
    title = request.GET.get("title")
    context = {"title": ""}

    if title is not None:
        title = title.strip()
        context["title"] = title
        if not title:
            context["blank_search"] = True
        else:
            try:
                results = openlibrary.search_books(title)
                context["books"] = results["books"]
                context["total"] = results["total"]
                # A comma-separated total for display, e.g. 21108 -> "21,108".
                context["total_display"] = f"{results['total']:,}"
                context["searched"] = True
            except openlibrary.OpenLibraryError as error:
                # Technical details go to the server log, never to the page.
                logger.warning("Open Library search failed for %r: %s", title, error)
                context["api_error"] = True

    return render(request, "books/search.html", context)


class BookListView(LoginRequiredMixin, ListView):
    """My Reading List: only the logged-in user's saved books, newest first."""

    template_name = "books/book_list.html"
    context_object_name = "books"

    def get_queryset(self):
        return SavedBook.objects.filter(user=self.request.user).order_by("-created_at")
