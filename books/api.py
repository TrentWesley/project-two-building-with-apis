"""Django REST Framework views for the reading list API (/api/...)."""

from rest_framework import generics

from .filters import filter_books
from .models import SavedBook
from .serializers import SavedBookSerializer


class BookListAPIView(generics.ListAPIView):
    """GET /api/books/: the logged-in user's saved books, 10 per page.

    Uses the same search (`q`), `status`, and `sort` rules as the My Reading List
    page, through the shared filter_books() helper.
    """

    serializer_class = SavedBookSerializer

    def get_queryset(self):
        """Only the requesting user's books, then the shared search/filter/sort."""
        my_books = SavedBook.objects.filter(user=self.request.user)
        return filter_books(
            my_books,
            search=self.request.query_params.get("q"),
            status=self.request.query_params.get("status"),
            sort=self.request.query_params.get("sort"),
        )


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """One of the logged-in user's saved books at /api/books/<id>/.

    GET shows it, PATCH changes its status, rating, and/or notes (the serializer
    ignores read-only Open Library fields), and DELETE removes it.
    Another user's book is not in get_queryset(), so every method returns 404.
    """

    serializer_class = SavedBookSerializer
    # PUT (replace the whole book) is left out on purpose, so it returns 405.
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_queryset(self):
        """Only the requesting user's books."""
        return SavedBook.objects.filter(user=self.request.user)
