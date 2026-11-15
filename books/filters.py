"""Shared search, filter, and sort rules for a user's saved books.

Used by the My Reading List page and the API list, so both behave the same.
"""

from django.db.models import Count, Q

from .models import SavedBook

# Each allowed "sort" value and the database ordering it uses.
# "-pk" breaks ties (same title, author, or save time), so the order is always the
# same and a book never appears on two pages.
SORT_ORDERS = {
    "newest": ["-created_at", "-pk"],
    "oldest": ["created_at", "pk"],
    "title": ["title", "-pk"],
    "author": ["author", "-pk"],
}
DEFAULT_SORT = "newest"

# The sort choices in the order the sidebar dropdown shows them.
SORT_CHOICES = [
    ("newest", "Newest saved"),
    ("oldest", "Oldest saved"),
    ("title", "Title (A–Z)"),
    ("author", "Author (A–Z)"),
]


def clean_search(search):
    """The search words without surrounding spaces ("" if missing)."""
    return (search or "").strip()


def clean_status(status):
    """The status if it is one of the three allowed codes, otherwise "" (all)."""
    if status in SavedBook.Status.values:
        return status
    return ""


def clean_sort(sort):
    """The sort if it is allowed, otherwise newest first."""
    if sort in SORT_ORDERS:
        return sort
    return DEFAULT_SORT


def filter_books(queryset, search, status, sort):
    """Return the books in `queryset` that match the search, status, and sort values.

    `queryset` must already contain only the logged-in user's books.
    Blank or unknown values never cause errors: an unknown status shows every
    status, and an unknown sort uses newest first.
    """
    search = clean_search(search)
    if search:
        # Q objects let us say "title contains the words OR author contains them".
        # icontains ignores capitalization.
        queryset = queryset.filter(
            Q(title__icontains=search) | Q(author__icontains=search)
        )

    status = clean_status(status)
    if status:
        queryset = queryset.filter(status=status)

    return queryset.order_by(*SORT_ORDERS[clean_sort(sort)])


def status_counts(queryset):
    """How many books in `queryset` have each status, plus the total (one query).

    Returns a dict like {"all": 12, "want_to_read": 5, "reading": 4, "finished": 3}.
    """
    counts = {"all": Count("pk")}
    for status in SavedBook.Status.values:
        counts[status] = Count("pk", filter=Q(status=status))
    return queryset.aggregate(**counts)
