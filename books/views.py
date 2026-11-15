import logging

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from . import openlibrary
from .forms import LoginForm, SaveBookForm, SignUpForm
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


def saved_work_keys(user, books):
    """The work keys from these search results that the user already saved (one query)."""
    keys_on_page = [book["work_key"] for book in books]
    return set(
        SavedBook.objects.filter(user=user, work_key__in=keys_on_page).values_list(
            "work_key", flat=True
        )
    )


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
                context["saved_work_keys"] = saved_work_keys(
                    request.user, results["books"]
                )
                # The Save forms send users back to this exact search.
                context["current_url"] = request.get_full_path()
                context["total"] = results["total"]
                # A comma-separated total for display, e.g. 21108 -> "21,108".
                context["total_display"] = f"{results['total']:,}"
                context["searched"] = True
            except openlibrary.OpenLibraryError as error:
                # Technical details go to the server log, never to the page.
                logger.warning("Open Library search failed for %r: %s", title, error)
                context["api_error"] = True

    return render(request, "books/search.html", context)


def safe_return_url(request):
    """The "next" URL from the form if it stays on this site, otherwise the search page."""
    next_url = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return next_url
    return reverse("search")


@login_required
@require_POST
def save_book(request):
    """Save one Open Library search result to the logged-in user's reading list."""
    form = SaveBookForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        already_saved = SavedBook.objects.filter(
            user=request.user, work_key=form.cleaned_data["work_key"]
        ).exists()

        if already_saved:
            messages.info(request, f"{title} is already in your reading list.")
        else:
            book = form.save(commit=False)
            # The owner always comes from the login, never from the form.
            book.user = request.user
            try:
                # The database's unique rule is the backstop: if two clicks arrive at
                # almost the same moment, the second one fails here instead of crashing.
                with transaction.atomic():
                    book.save()
            except IntegrityError:
                messages.info(request, f"{title} is already in your reading list.")
            else:
                messages.success(request, f"Saved {title} to your reading list.")
    else:
        messages.error(
            request,
            "Sorry, that book couldn't be saved because its details were invalid.",
        )
    return redirect(safe_return_url(request))


class BookListView(LoginRequiredMixin, ListView):
    """My Reading List: only the logged-in user's saved books, newest first."""

    template_name = "books/book_list.html"
    context_object_name = "books"

    def get_queryset(self):
        return SavedBook.objects.filter(user=self.request.user).order_by("-created_at")
