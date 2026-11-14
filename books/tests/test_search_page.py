import pytest
from django.contrib.auth.models import User

from books import openlibrary

TEST_PASSWORD = "Test-only-pass-2026!"


@pytest.fixture
def reader(db):
    return User.objects.create_user(username="reader1", password=TEST_PASSWORD)


def test_blank_search_shows_message_without_calling_open_library(
    client, reader, monkeypatch
):
    calls = []

    def fake_search_books(title):
        calls.append(title)
        return {"total": 0, "books": []}

    # Replace the real Open Library call so the test can see whether it was used.
    monkeypatch.setattr(openlibrary, "search_books", fake_search_books, raising=False)
    client.force_login(reader)

    for blank_title in ["", "   "]:
        response = client.get("/search/", {"title": blank_title})
        assert response.status_code == 200
        assert "Please enter a book title." in response.content.decode()

    assert calls == []


def test_open_library_failure_shows_friendly_alert(client, reader, monkeypatch):
    def failing_search_books(title):
        raise openlibrary.OpenLibraryError("ConnectTimeout: technical details here")

    monkeypatch.setattr(
        openlibrary, "search_books", failing_search_books, raising=False
    )
    client.force_login(reader)

    response = client.get("/search/", {"title": "dune"})
    content = response.content.decode()

    assert response.status_code == 200
    assert "Sorry, we couldn't reach Open Library right now." in content
    assert "technical details here" not in content


def fake_results(total, books):
    """Build a fake search_books() that returns the given results."""

    def fake_search_books(title):
        return {"total": total, "books": books}

    return fake_search_books


DUNE = {
    "work_key": "/works/OL893414W",
    "title": "Dune",
    "author": "Frank Herbert",
    "first_publish_year": 1965,
    "cover_id": 11481354,
}
NO_DETAILS = {
    "work_key": "/works/OL1W",
    "title": "Unknown title",
    "author": "Unknown author",
    "first_publish_year": None,
    "cover_id": None,
}


@pytest.mark.django_db
def test_search_page_requires_login(client):
    response = client.get("/search/")

    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/search/"


def test_first_visit_shows_form_without_messages_or_api_call(
    client, reader, monkeypatch
):
    calls = []
    monkeypatch.setattr(
        openlibrary, "search_books", lambda title: calls.append(title), raising=False
    )
    client.force_login(reader)

    content = client.get("/search/").content.decode()

    assert 'name="title"' in content
    assert "Please enter a book title." not in content
    assert calls == []


def test_search_results_show_total_cards_and_placeholders(client, reader, monkeypatch):
    monkeypatch.setattr(
        openlibrary, "search_books", fake_results(21108, [DUNE, NO_DETAILS])
    )
    client.force_login(reader)

    content = client.get("/search/", {"title": "dune"}).content.decode()

    assert "Found 21,108 matches." in content
    assert "Showing the first 2." in content
    assert "Frank Herbert" in content
    assert "1965" in content
    assert "https://covers.openlibrary.org/b/id/11481354-M.jpg" in content
    assert "Unknown title" in content
    assert "Unknown author" in content
    assert "Year unknown" in content
    assert "No cover" in content


def test_one_result_uses_singular_wording(client, reader, monkeypatch):
    monkeypatch.setattr(openlibrary, "search_books", fake_results(1, [DUNE]))
    client.force_login(reader)

    content = client.get("/search/", {"title": "dune"}).content.decode()

    assert "Found 1 match." in content
    assert "Showing the first 1." in content


def test_no_results_shows_message_with_search_term(client, reader, monkeypatch):
    monkeypatch.setattr(openlibrary, "search_books", fake_results(0, []))
    client.force_login(reader)

    content = client.get("/search/", {"title": "xyzqqnotabook"}).content.decode()

    assert 'No books found for "xyzqqnotabook".' in content


def test_search_term_is_stripped_before_searching(client, reader, monkeypatch):
    calls = []

    def recording_search(title):
        calls.append(title)
        return {"total": 0, "books": []}

    monkeypatch.setattr(openlibrary, "search_books", recording_search)
    client.force_login(reader)

    client.get("/search/", {"title": "  dune  "})

    assert calls == ["dune"]


def test_open_library_failure_is_logged_for_the_developer(
    client, reader, monkeypatch, caplog
):
    def failing_search_books(title):
        raise openlibrary.OpenLibraryError("ConnectTimeout: technical details here")

    monkeypatch.setattr(openlibrary, "search_books", failing_search_books)
    client.force_login(reader)

    client.get("/search/", {"title": "dune"})

    assert "technical details here" in caplog.text
