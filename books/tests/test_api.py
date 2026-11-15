"""Tests for the reading list API (/api/books/)."""

from datetime import UTC, datetime
from urllib.parse import parse_qs, urlsplit

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from books.models import SavedBook

API_LIST_URL = "/api/books/"
TEST_PASSWORD = "Test-only-pass-2026!"

# The fields the approved serializer shows. `user` must never appear.
APPROVED_FIELDS = {
    "id",
    "work_key",
    "title",
    "author",
    "first_publish_year",
    "cover_id",
    "status",
    "rating",
    "notes",
    "created_at",
}


def add_book(user, number, title, author="Some Author", **extra):
    """Save a book for this user with a unique, valid work key."""
    return SavedBook.objects.create(
        user=user, work_key=f"/works/OL{number}W", title=title, author=author, **extra
    )


def token_header(user):
    """The Authorization header for a real DRF token belonging to this user."""
    token = Token.objects.create(user=user)
    return {"HTTP_AUTHORIZATION": f"Token {token.key}"}


@pytest.mark.django_db
def test_requests_without_a_valid_token_get_401(client):
    """No token, or a made-up token, means 401 Unauthorized (not 403)."""
    no_token = client.get(API_LIST_URL)
    bad_token = client.get(API_LIST_URL, HTTP_AUTHORIZATION="Token not-a-real-token")

    assert no_token.status_code == 401
    assert bad_token.status_code == 401
    # A 401 tells the client how to log in: send a token.
    assert no_token.headers["WWW-Authenticate"] == "Token"


@pytest.mark.django_db
def test_token_user_gets_only_their_books_10_per_page(client):
    """A valid token lists only that user's books, in DRF's paginated format."""
    reader = User.objects.create_user(username="reader1", password=TEST_PASSWORD)
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    my_titles = {add_book(reader, n, f"My Book {n}").title for n in range(1, 13)}
    other_titles = {
        add_book(other_reader, n, f"Other Book {n}").title for n in range(101, 105)
    }
    auth = token_header(reader)

    page_1 = client.get(API_LIST_URL, **auth)
    page_2 = client.get(API_LIST_URL, {"page": 2}, **auth)

    assert page_1.status_code == 200
    assert page_2.status_code == 200
    data_1 = page_1.json()
    data_2 = page_2.json()

    # DRF's page-number format, counting only my 12 books (not all 16).
    assert isinstance(data_1, dict)
    assert set(data_1) == {"count", "next", "previous", "results"}
    assert data_1["count"] == 12
    assert data_1["previous"] is None
    assert data_1["next"] is not None
    assert data_2["next"] is None
    assert data_2["previous"] is not None

    # 10 on page 1, the remaining 2 on page 2.
    assert len(data_1["results"]) == 10
    assert len(data_2["results"]) == 2

    # Together the two pages are exactly my books, with none of reader2's.
    titles = [book["title"] for book in data_1["results"] + data_2["results"]]
    assert set(titles) == my_titles
    assert not set(titles) & other_titles

    # Each book shows exactly the approved fields (no `user`).
    assert set(data_1["results"][0]) == APPROVED_FIELDS


@pytest.mark.django_db
def test_detail_shows_my_book_but_404_for_another_users_book(client):
    """A token user can open their own book, but another user's book is 404."""
    reader = User.objects.create_user(username="reader1", password=TEST_PASSWORD)
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    my_book = add_book(reader, 1, "My Book")
    their_book = add_book(other_reader, 2, "Their Book")
    auth = token_header(reader)

    mine = client.get(f"{API_LIST_URL}{my_book.pk}/", **auth)
    theirs = client.get(f"{API_LIST_URL}{their_book.pk}/", **auth)

    # My own book works. (This also proves the 404 below comes from the
    # ownership rule, not from a missing URL.)
    assert mine.status_code == 200
    assert mine.json()["title"] == "My Book"
    assert set(mine.json()) == APPROVED_FIELDS

    # Another user's book looks like it doesn't exist.
    assert theirs.status_code == 404
    assert "Their Book" not in theirs.content.decode()


# --- Search, filter, sort, and pagination (shared filter_books() helper) ---


@pytest.fixture
def reader(db):
    return User.objects.create_user(username="reader1", password=TEST_PASSWORD)


@pytest.fixture
def auth(reader):
    """Token header for reader1."""
    return token_header(reader)


@pytest.fixture
def three_books(reader):
    """Three of reader1's books whose title, author, and date orders all differ.

    Newest first: Cloud Atlas, Anathem, Brave New World
    By title:     Anathem, Brave New World, Cloud Atlas
    By author:    Brave New World (Aldous), Cloud Atlas (David), Anathem (Neal)
    (The same books as the website's filter tests.)
    """
    books = [
        ("Anathem", "Neal Stephenson", SavedBook.Status.FINISHED, 2),
        ("Brave New World", "Aldous Huxley", SavedBook.Status.READING, 1),
        ("Cloud Atlas", "David Mitchell", SavedBook.Status.WANT_TO_READ, 3),
    ]
    for number, (title, author, status, month) in enumerate(books, start=1):
        book = add_book(reader, number, title, author, status=status)
        # Clearly different save dates, so the order never depends on clock precision.
        SavedBook.objects.filter(pk=book.pk).update(
            created_at=datetime(2026, month, 1, tzinfo=UTC)
        )
    # Another user's book: it would come first in every order if it ever leaked in.
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    other_book = add_book(other_reader, 99, "Aardvark Tales", "Aaron Abbott")
    SavedBook.objects.filter(pk=other_book.pk).update(
        created_at=datetime(2026, 12, 1, tzinfo=UTC)
    )


def api_titles(response):
    return [book["title"] for book in response.json()["results"]]


NEWEST_FIRST = ["Cloud Atlas", "Anathem", "Brave New World"]


@pytest.mark.parametrize(
    ("params", "expected_titles"),
    [
        # Search matches title OR author, ignoring capitals and outer spaces.
        ({"q": "  HUXLEY  "}, ["Brave New World"]),
        ({"q": "atlas"}, ["Cloud Atlas"]),
        ({"q": "d"}, ["Cloud Atlas", "Brave New World"]),
        # Another user's book is never found, even by an exact search.
        ({"q": "Aardvark"}, []),
        # Each status filters.
        ({"status": "want_to_read"}, ["Cloud Atlas"]),
        ({"status": "reading"}, ["Brave New World"]),
        ({"status": "finished"}, ["Anathem"]),
        # Each sort option.
        ({"sort": "newest"}, NEWEST_FIRST),
        ({"sort": "oldest"}, ["Brave New World", "Anathem", "Cloud Atlas"]),
        ({"sort": "title"}, ["Anathem", "Brave New World", "Cloud Atlas"]),
        ({"sort": "author"}, ["Brave New World", "Cloud Atlas", "Anathem"]),
        # Search, status, and sort together.
        ({"q": "d", "status": "reading", "sort": "title"}, ["Brave New World"]),
        # Blank or invalid values are ignored: all my books, newest first.
        ({}, NEWEST_FIRST),
        ({"q": "   "}, NEWEST_FIRST),
        ({"status": "xyz"}, NEWEST_FIRST),
        ({"status": ""}, NEWEST_FIRST),
        ({"sort": "banana"}, NEWEST_FIRST),
        ({"sort": ""}, NEWEST_FIRST),
    ],
)
def test_api_search_filter_and_sort_match_the_website(
    client, auth, three_books, params, expected_titles
):
    """The API uses the same q/status/sort rules as the My Reading List page."""
    response = client.get(API_LIST_URL, params, **auth)

    assert response.status_code == 200
    assert api_titles(response) == expected_titles
    # The count also reflects the filter (only matching books of mine).
    assert response.json()["count"] == len(expected_titles)


def test_api_and_website_list_the_same_books_in_the_same_order(
    client, reader, auth, three_books
):
    """Same parameters, same result on both sides (they share filter_books)."""
    params = {"q": "a", "sort": "author"}
    api_response = client.get(API_LIST_URL, params, **auth)
    client.force_login(reader)
    page_response = client.get("/books/", params)

    website_titles = [book.title for book in page_response.context["books"]]
    assert api_titles(api_response) == website_titles


def query_of(url):
    """The query parameters of a pagination link, as a simple dict."""
    return {name: values[0] for name, values in parse_qs(urlsplit(url).query).items()}


def test_pagination_links_keep_search_status_and_sort(client, reader, auth):
    """next/previous links keep q, status, and sort, and only change the page."""
    for number in range(1, 13):
        add_book(reader, number, f"Finished Book {number:02}", status="finished")
    add_book(reader, 50, "Unread Book", status="want_to_read")
    params = {"q": "book", "status": "finished", "sort": "title"}

    page_1 = client.get(API_LIST_URL, params, **auth)
    page_2 = client.get(API_LIST_URL, {**params, "page": 2}, **auth)

    assert page_1.json()["count"] == 12
    assert query_of(page_1.json()["next"]) == {**params, "page": "2"}
    # DRF leaves "page" out of the link back to page 1.
    assert query_of(page_2.json()["previous"]) == params
    # 10 + 2 books, sorted by title across both pages.
    all_titles = api_titles(page_1) + api_titles(page_2)
    assert all_titles == [f"Finished Book {n:02}" for n in range(1, 13)]


def test_books_saved_at_the_same_moment_never_repeat_across_pages(client, reader, auth):
    """Ties are broken by id, so every book appears exactly once (stable order)."""
    for number in range(1, 13):
        add_book(reader, number, "Same Title")
    SavedBook.objects.update(created_at=datetime(2026, 5, 1, tzinfo=UTC))

    page_1 = client.get(API_LIST_URL, **auth).json()
    page_2 = client.get(API_LIST_URL, {"page": 2}, **auth).json()

    ids = [book["id"] for book in page_1["results"] + page_2["results"]]
    assert len(ids) == 12
    assert ids == sorted(ids, reverse=True)


@pytest.mark.parametrize("bad_page", ["abc", "0", "-1", "999", "2.5"])
def test_bad_page_values_get_drf_404_not_a_server_error(
    client, auth, three_books, bad_page
):
    """A bad page gets DRF's standard "Invalid page." 404 instead of a crash."""
    response = client.get(API_LIST_URL, {"page": bad_page}, **auth)

    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid page."}


# --- Other authentication checks ---


def test_logged_in_website_user_can_use_the_api_with_their_session(
    client, reader, three_books
):
    """Session login (no token) works, so the browsable API is usable."""
    client.force_login(reader)

    response = client.get(API_LIST_URL)

    assert response.status_code == 200
    assert api_titles(response) == NEWEST_FIRST


def test_browsable_api_page_renders_for_a_logged_in_user(client, reader, three_books):
    """Opening the API in a browser shows DRF's HTML page, not raw JSON."""
    client.force_login(reader)

    response = client.get(API_LIST_URL, HTTP_ACCEPT="text/html")

    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]
    assert "Cloud Atlas" in response.content.decode()


def test_detail_without_a_token_gets_401(client, three_books):
    """The detail endpoint also requires login."""
    book = SavedBook.objects.get(title="Cloud Atlas")

    response = client.get(f"{API_LIST_URL}{book.pk}/")

    assert response.status_code == 401
    assert "Cloud Atlas" not in response.content.decode()
