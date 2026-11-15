import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.db.models.query import QuerySet

from books.models import SavedBook

TEST_PASSWORD = "Test-only-pass-2026!"

# What a Save form on the search page submits for Dune.
DUNE_FORM = {
    "work_key": "/works/OL893414W",
    "title": "Dune",
    "author": "Frank Herbert",
    "first_publish_year": "1965",
    "cover_id": "11481354",
    "next": "/search/?title=dune",
}


@pytest.fixture
def reader(db):
    return User.objects.create_user(username="reader1", password=TEST_PASSWORD)


def message_texts(response):
    """The messages Django queued for the next page."""
    return [str(message) for message in get_messages(response.wsgi_request)]


def test_saving_a_valid_book_adds_it_to_my_list_as_want_to_read(client, reader):
    client.force_login(reader)

    response = client.post("/books/save/", DUNE_FORM)

    my_books = SavedBook.objects.filter(user=reader)
    assert my_books.count() == 1
    book = my_books.get()
    assert book.work_key == "/works/OL893414W"
    assert book.status == SavedBook.Status.WANT_TO_READ
    assert book.title == "Dune"
    assert book.author == "Frank Herbert"
    assert book.first_publish_year == 1965
    assert book.cover_id == 11481354
    assert response.status_code == 302
    assert response.url == "/search/?title=dune"
    assert "Saved Dune to your reading list." in message_texts(response)


def test_saving_the_same_book_twice_shows_friendly_message_and_no_duplicate(
    client, reader
):
    # Show any server error as a 500 page (like a real browser) instead of raising it.
    client.raise_request_exception = False
    client.force_login(reader)
    client.post("/books/save/", DUNE_FORM)

    response = client.post("/books/save/", DUNE_FORM)

    assert response.status_code == 302
    assert response.url == "/search/?title=dune"
    assert "Dune is already in your reading list." in message_texts(response)
    assert SavedBook.objects.filter(user=reader).count() == 1


@pytest.mark.parametrize(
    "bad_work_key",
    ["abc", "/books/OL123M", "", "/works/OLW"],
    ids=["plain-text", "edition-key", "empty", "missing-number"],
)
def test_invalid_work_key_is_rejected_without_saving(client, reader, bad_work_key):
    client.raise_request_exception = False
    client.force_login(reader)

    response = client.post("/books/save/", {**DUNE_FORM, "work_key": bad_work_key})

    assert response.status_code == 302
    assert response.url == "/search/?title=dune"
    assert SavedBook.objects.filter(user=reader).count() == 0
    assert (
        "Sorry, that book couldn't be saved because its details were invalid."
        in message_texts(response)
    )


@pytest.mark.django_db
def test_saving_requires_login(client):
    response = client.post("/books/save/", DUNE_FORM)

    assert response.status_code == 302
    assert response.url.startswith("/accounts/login/")
    assert SavedBook.objects.count() == 0


def test_get_request_to_save_is_not_allowed(client, reader):
    client.force_login(reader)

    response = client.get("/books/save/")

    assert response.status_code == 405
    assert SavedBook.objects.count() == 0


def test_submitted_user_id_cannot_change_the_owner(client, reader):
    someone_else = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    client.force_login(reader)

    client.post("/books/save/", {**DUNE_FORM, "user": someone_else.pk})

    book = SavedBook.objects.get(work_key="/works/OL893414W")
    assert book.user == reader
    assert not SavedBook.objects.filter(user=someone_else).exists()


def test_unsafe_next_url_falls_back_to_search_page(client, reader):
    client.force_login(reader)

    response = client.post(
        "/books/save/", {**DUNE_FORM, "next": "https://evil.example.com/"}
    )

    assert response.status_code == 302
    assert response.url == "/search/"


def test_different_users_can_save_the_same_work(client, reader):
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)

    client.force_login(reader)
    client.post("/books/save/", DUNE_FORM)
    client.force_login(other_reader)
    response = client.post("/books/save/", DUNE_FORM)

    assert "Saved Dune to your reading list." in message_texts(response)
    assert SavedBook.objects.filter(work_key="/works/OL893414W").count() == 2


def test_near_simultaneous_duplicate_is_caught_by_database_rule(
    client, reader, monkeypatch
):
    """If two clicks race past the "already saved?" check, the database rule still wins."""
    SavedBook.objects.create(
        user=reader, work_key="/works/OL893414W", title="Dune", author="Frank Herbert"
    )
    # Pretend the "already saved?" check missed the existing book.
    monkeypatch.setattr(QuerySet, "exists", lambda self: False)
    client.raise_request_exception = False
    client.force_login(reader)

    response = client.post("/books/save/", DUNE_FORM)

    assert response.status_code == 302
    assert "Dune is already in your reading list." in message_texts(response)
    monkeypatch.undo()
    assert SavedBook.objects.filter(user=reader).count() == 1


def test_invalid_publication_year_shows_friendly_error(client, reader):
    client.force_login(reader)

    response = client.post(
        "/books/save/", {**DUNE_FORM, "first_publish_year": "nineteen sixty-five"}
    )

    assert response.status_code == 302
    assert SavedBook.objects.count() == 0
    assert (
        "Sorry, that book couldn't be saved because its details were invalid."
        in message_texts(response)
    )


def test_book_without_year_or_cover_can_be_saved(client, reader):
    client.force_login(reader)

    client.post("/books/save/", {**DUNE_FORM, "first_publish_year": "", "cover_id": ""})

    book = SavedBook.objects.get(user=reader)
    assert book.first_publish_year is None
    assert book.cover_id is None
