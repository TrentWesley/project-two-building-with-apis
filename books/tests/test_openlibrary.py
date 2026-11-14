import pytest
import requests

from books import openlibrary
from books.openlibrary import clean_book


@pytest.mark.parametrize(
    ("raw_doc", "expected"),
    [
        # A complete result: every field present, two authors joined with commas.
        (
            {
                "key": "/works/OL453936W",
                "title": "Good Omens",
                "author_name": ["Terry Pratchett", "Neil Gaiman"],
                "first_publish_year": 1990,
                "cover_i": 10482258,
            },
            {
                "work_key": "/works/OL453936W",
                "title": "Good Omens",
                "author": "Terry Pratchett, Neil Gaiman",
                "first_publish_year": 1990,
                "cover_id": 10482258,
            },
        ),
        # Missing title, author, year, and cover.
        (
            {"key": "/works/OL1W"},
            {
                "work_key": "/works/OL1W",
                "title": "Unknown title",
                "author": "Unknown author",
                "first_publish_year": None,
                "cover_id": None,
            },
        ),
        # An author list that is present but empty.
        (
            {"key": "/works/OL2W", "title": "Dune", "author_name": []},
            {
                "work_key": "/works/OL2W",
                "title": "Dune",
                "author": "Unknown author",
                "first_publish_year": None,
                "cover_id": None,
            },
        ),
    ],
    ids=["complete", "missing-fields", "empty-author-list"],
)
def test_clean_book_normalizes_open_library_results(raw_doc, expected):
    assert clean_book(raw_doc) == expected


class FakeResponse:
    """A stand-in for requests' Response object."""

    def __init__(self, data=None, status_error=None, json_error=None):
        self.data = data
        self.status_error = status_error
        self.json_error = json_error

    def raise_for_status(self):
        if self.status_error:
            raise self.status_error

    def json(self):
        if self.json_error:
            raise self.json_error
        return self.data


def test_search_books_sends_approved_request_and_returns_clean_results(monkeypatch):
    sent = {}

    def fake_get(url, params, headers, timeout):
        sent.update(url=url, params=params, headers=headers, timeout=timeout)
        return FakeResponse(
            {
                "numFound": 21108,
                "docs": [
                    {
                        "key": "/works/OL893414W",
                        "title": "Dune",
                        "author_name": ["Frank Herbert"],
                    }
                ],
            }
        )

    monkeypatch.setattr(requests, "get", fake_get)

    results = openlibrary.search_books("dune")

    assert sent["url"] == "https://openlibrary.org/search.json"
    assert sent["params"] == {
        "title": "dune",
        "fields": "key,title,author_name,first_publish_year,cover_i",
        "limit": 10,
    }
    assert sent["headers"] == {"User-Agent": "CIDM3312-BookSearch/1.0"}
    assert sent["timeout"] == 10
    assert results["total"] == 21108
    assert results["books"][0]["title"] == "Dune"
    assert results["books"][0]["author"] == "Frank Herbert"


@pytest.mark.parametrize(
    "make_failure",
    [
        lambda: requests.exceptions.ConnectionError("no connection"),
        lambda: requests.exceptions.Timeout("took too long"),
    ],
    ids=["connection-error", "timeout"],
)
def test_search_books_turns_network_errors_into_open_library_error(
    monkeypatch, make_failure
):
    def failing_get(*args, **kwargs):
        raise make_failure()

    monkeypatch.setattr(requests, "get", failing_get)

    with pytest.raises(openlibrary.OpenLibraryError):
        openlibrary.search_books("dune")


def test_search_books_turns_http_errors_into_open_library_error(monkeypatch):
    error = requests.exceptions.HTTPError("503 Server Error")
    monkeypatch.setattr(
        requests, "get", lambda *args, **kwargs: FakeResponse(status_error=error)
    )

    with pytest.raises(openlibrary.OpenLibraryError):
        openlibrary.search_books("dune")


@pytest.mark.parametrize(
    "response",
    [
        FakeResponse(json_error=ValueError("not JSON")),
        FakeResponse(data=["not", "a", "dictionary"]),
    ],
    ids=["invalid-json", "unexpected-shape"],
)
def test_search_books_turns_bad_responses_into_open_library_error(
    monkeypatch, response
):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: response)

    with pytest.raises(openlibrary.OpenLibraryError):
        openlibrary.search_books("dune")
