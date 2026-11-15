"""Tests for script 2 (api_script.py).

HTTP and input() are faked with pytest's monkeypatch, so no server or real
token is ever needed.
"""

import pytest
import requests

import api_script


@pytest.fixture
def sent_requests(monkeypatch):
    """Record every HTTP request the script tries to send (none really go out)."""
    calls = []

    def fake_request(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("The script sent an HTTP request.")

    monkeypatch.setattr(requests, "get", fake_request)
    monkeypatch.setattr(requests, "patch", fake_request)
    return calls


@pytest.mark.parametrize("token_value", [None, "", "   "])
def test_missing_token_prints_setup_message_and_sends_no_request(
    monkeypatch, capsys, sent_requests, token_value
):
    """No token (unset, empty, or only spaces) means a setup message, no request."""
    if token_value is None:
        monkeypatch.delenv("READING_LIST_TOKEN", raising=False)
    else:
        monkeypatch.setenv("READING_LIST_TOKEN", token_value)

    def fail_input(prompt=""):
        raise AssertionError("The script asked for input without a token.")

    monkeypatch.setattr("builtins.input", fail_input)

    api_script.main()

    output = capsys.readouterr().out
    assert "READING_LIST_TOKEN is not set" in output
    assert "drf_create_token" in output
    assert sent_requests == []


# --- Fakes for a successful run ---

FAKE_TOKEN = "fake-test-token"  # Not a real token; tests never use one.


class FakeResponse:
    """Just enough of requests.Response for the script."""

    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error", response=self)


TWO_BOOKS_PAGE = {
    "count": 2,
    "next": None,
    "previous": None,
    "results": [
        {"id": 12, "title": "Dune", "status": "want_to_read"},
        {"id": 7, "title": "The Hobbit", "status": "reading"},
    ],
}


def fake_inputs(monkeypatch, answers):
    """Make input() return these answers in order."""
    answers = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))


def test_successful_run_lists_books_and_shows_before_and_after(monkeypatch, capsys):
    """List my books, pick one, PATCH its status, and show Before/After."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    monkeypatch.delenv("READING_LIST_API_URL", raising=False)
    calls = []

    def fake_get(url, **kwargs):
        calls.append(("GET", url, kwargs))
        return FakeResponse(200, TWO_BOOKS_PAGE)

    def fake_patch(url, **kwargs):
        calls.append(("PATCH", url, kwargs))
        return FakeResponse(200, {"id": 12, "title": "Dune", "status": "finished"})

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(requests, "patch", fake_patch)
    fake_inputs(monkeypatch, ["12", "finished"])

    api_script.main()

    output = capsys.readouterr().out
    # The list: first-page note, then each book's ID, title, and status.
    assert "Showing the first page only" in output
    assert "[12] Dune - want_to_read" in output
    assert "[7] The Hobbit - reading" in output
    # Before comes from the list; After comes from the PATCH response.
    assert "Before: want_to_read" in output
    assert "After: finished" in output

    # Exactly one GET of the list, then one PATCH of book 12.
    assert [(method, url) for method, url, _ in calls] == [
        ("GET", "http://127.0.0.1:8000/api/books/"),
        ("PATCH", "http://127.0.0.1:8000/api/books/12/"),
    ]
    patch_kwargs = calls[1][2]
    assert patch_kwargs["json"] == {"status": "finished"}
    for _, _, kwargs in calls:
        assert kwargs["headers"] == {"Authorization": f"Token {FAKE_TOKEN}"}
        assert kwargs["timeout"] == 10


def test_patch_404_prints_friendly_message_without_before_or_after(monkeypatch, capsys):
    """A PATCH 404 (missing or not my book) is a friendly message, not a crash."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    monkeypatch.delenv("READING_LIST_API_URL", raising=False)
    calls = []

    def fake_get(url, **kwargs):
        calls.append(("GET", url))
        return FakeResponse(200, TWO_BOOKS_PAGE)

    def fake_patch(url, **kwargs):
        calls.append(("PATCH", url))
        return FakeResponse(404, {"detail": "No SavedBook matches the given query."})

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(requests, "patch", fake_patch)
    fake_inputs(monkeypatch, ["99", "finished"])

    try:
        api_script.main()
    except requests.RequestException as error:
        pytest.fail(f"The script crashed instead of showing a message: {error!r}")

    output = capsys.readouterr().out
    assert "No book with ID 99 in your reading list." in output.splitlines()
    assert "Before:" not in output
    assert "After:" not in output
    # Only the faked requests were made (nothing reached a real server).
    assert calls == [
        ("GET", "http://127.0.0.1:8000/api/books/"),
        ("PATCH", "http://127.0.0.1:8000/api/books/99/"),
    ]


# --- Invalid input is caught before any PATCH ---


@pytest.mark.parametrize(
    ("answers", "expected_message"),
    [
        (["abc", "finished"], '"abc" is not a valid book ID. Enter a number, like 12.'),
        (["", "finished"], "Please enter a book ID."),
        (["12", "abandoned"], '"abandoned" is not a valid status.'),
        (["12", ""], "Please enter a status."),
    ],
)
def test_invalid_id_or_status_shows_message_and_sends_no_patch(
    monkeypatch, capsys, answers, expected_message
):
    """A bad book ID or status gets a specific message, and no PATCH is sent."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    monkeypatch.delenv("READING_LIST_API_URL", raising=False)
    patch_calls = []

    def fake_get(url, **kwargs):
        return FakeResponse(200, TWO_BOOKS_PAGE)

    def fake_patch(url, **kwargs):
        patch_calls.append(url)
        return FakeResponse(404, {"detail": "Not found."})

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(requests, "patch", fake_patch)
    fake_inputs(monkeypatch, answers)

    api_script.main()

    output = capsys.readouterr().out
    assert expected_message in output
    assert patch_calls == []
    assert "Before:" not in output
    assert "After:" not in output


def test_invalid_status_message_lists_the_allowed_statuses(monkeypatch, capsys):
    """The status message tells the user exactly what they can type."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    monkeypatch.setattr(
        requests, "get", lambda url, **kwargs: FakeResponse(200, TWO_BOOKS_PAGE)
    )
    monkeypatch.setattr(requests, "patch", lambda url, **kwargs: FakeResponse(404, {}))
    fake_inputs(monkeypatch, ["12", "done"])

    api_script.main()

    output = capsys.readouterr().out
    assert "Choose one of: want_to_read, reading, finished" in output


# --- HTTP 401: the token was rejected ---


def run_without_crashing():
    """Run the script; a requests error escaping main() fails the test."""
    try:
        api_script.main()
    except requests.RequestException as error:
        pytest.fail(f"The script crashed instead of showing a message: {error!r}")


def test_list_401_shows_token_rejected_message_and_stops(monkeypatch, capsys):
    """A 401 on the list: friendly message, no input, no PATCH, token not shown."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    patch_calls = []

    def fake_get(url, **kwargs):
        return FakeResponse(401, {"detail": "Invalid token."})

    def fake_patch(url, **kwargs):
        patch_calls.append(url)
        return FakeResponse(200, {})

    def fail_input(prompt=""):
        raise AssertionError("The script asked for input after a 401.")

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(requests, "patch", fake_patch)
    monkeypatch.setattr("builtins.input", fail_input)

    run_without_crashing()

    output = capsys.readouterr().out
    assert "Your API token was rejected" in output
    assert "READING_LIST_TOKEN" in output
    assert FAKE_TOKEN not in output
    assert patch_calls == []
    assert "Before:" not in output
    assert "After:" not in output


def test_patch_401_shows_token_rejected_message_and_stops(monkeypatch, capsys):
    """A 401 on the PATCH: friendly message, no Before/After, token not shown."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    monkeypatch.setattr(
        requests, "get", lambda url, **kwargs: FakeResponse(200, TWO_BOOKS_PAGE)
    )
    monkeypatch.setattr(
        requests,
        "patch",
        lambda url, **kwargs: FakeResponse(401, {"detail": "Invalid token."}),
    )
    fake_inputs(monkeypatch, ["12", "finished"])

    run_without_crashing()

    output = capsys.readouterr().out
    assert "Your API token was rejected" in output
    assert FAKE_TOKEN not in output
    assert "Before:" not in output
    assert "After:" not in output


# --- Connection errors: the Django server can't be reached ---


def refuse_connection(url, **kwargs):
    """Act like the Django server isn't running."""
    raise requests.ConnectionError("Connection refused")


def test_list_connection_error_shows_message_and_stops(monkeypatch, capsys):
    """Server unreachable on the list: friendly message, no input, no PATCH."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    patch_calls = []

    def fake_patch(url, **kwargs):
        patch_calls.append(url)
        return FakeResponse(200, {})

    def fail_input(prompt=""):
        raise AssertionError("The script asked for input after a connection error.")

    monkeypatch.setattr(requests, "get", refuse_connection)
    monkeypatch.setattr(requests, "patch", fake_patch)
    monkeypatch.setattr("builtins.input", fail_input)

    run_without_crashing()

    output = capsys.readouterr().out
    assert "Could not reach the reading list API" in output
    assert "Django development server is running" in output
    assert FAKE_TOKEN not in output
    assert patch_calls == []
    assert "Before:" not in output
    assert "After:" not in output


def test_patch_connection_error_shows_message_and_stops(monkeypatch, capsys):
    """Server unreachable on the PATCH: friendly message, no Before/After."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    monkeypatch.setattr(
        requests, "get", lambda url, **kwargs: FakeResponse(200, TWO_BOOKS_PAGE)
    )
    monkeypatch.setattr(requests, "patch", refuse_connection)
    fake_inputs(monkeypatch, ["12", "finished"])

    run_without_crashing()

    output = capsys.readouterr().out
    assert "Could not reach the reading list API" in output
    assert "Django development server is running" in output
    assert FAKE_TOKEN not in output
    assert "Before:" not in output
    assert "After:" not in output


# --- An empty reading list ---


def test_empty_list_shows_message_and_asks_nothing(monkeypatch, capsys):
    """No saved books: a friendly message, no questions, and no PATCH."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    empty_page = {"count": 0, "next": None, "previous": None, "results": []}
    patch_calls = []
    input_prompts = []

    def fake_patch(url, **kwargs):
        patch_calls.append(url)
        return FakeResponse(200, {})

    def record_input(prompt=""):
        input_prompts.append(prompt)
        return ""

    monkeypatch.setattr(
        requests, "get", lambda url, **kwargs: FakeResponse(200, empty_page)
    )
    monkeypatch.setattr(requests, "patch", fake_patch)
    monkeypatch.setattr("builtins.input", record_input)

    run_without_crashing()

    output = capsys.readouterr().out
    assert "Your reading list is empty." in output
    assert "website" in output
    assert input_prompts == []
    assert patch_calls == []
    assert "Before:" not in output
    assert "After:" not in output


# --- Invalid JSON: a 200 response whose body isn't JSON ---


class BadJSONResponse(FakeResponse):
    """A 200 response whose body can't be read as JSON (for example, an HTML page)."""

    def __init__(self):
        super().__init__(200, None)

    def json(self):
        raise requests.JSONDecodeError("Expecting value", "<html>Oops</html>", 0)


def test_list_invalid_json_shows_message_and_stops(monkeypatch, capsys):
    """A list response that isn't JSON: friendly message, no input, no PATCH."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    patch_calls = []

    def fake_patch(url, **kwargs):
        patch_calls.append(url)
        return FakeResponse(200, {})

    def fail_input(prompt=""):
        raise AssertionError("The script asked for input after invalid JSON.")

    monkeypatch.setattr(requests, "get", lambda url, **kwargs: BadJSONResponse())
    monkeypatch.setattr(requests, "patch", fake_patch)
    monkeypatch.setattr("builtins.input", fail_input)

    run_without_crashing()

    output = capsys.readouterr().out
    assert "The API returned an invalid response" in output
    assert FAKE_TOKEN not in output
    assert patch_calls == []
    assert "Before:" not in output
    assert "After:" not in output


def test_patch_invalid_json_shows_message_and_stops(monkeypatch, capsys):
    """A PATCH response that isn't JSON: friendly message, no Before/After."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    monkeypatch.setattr(
        requests, "get", lambda url, **kwargs: FakeResponse(200, TWO_BOOKS_PAGE)
    )
    monkeypatch.setattr(requests, "patch", lambda url, **kwargs: BadJSONResponse())
    fake_inputs(monkeypatch, ["12", "finished"])

    run_without_crashing()

    output = capsys.readouterr().out
    assert "The API returned an invalid response" in output
    assert FAKE_TOKEN not in output
    assert "Before:" not in output
    assert "After:" not in output


# --- HTTP 500: the API had a server error ---


def test_list_500_shows_server_error_message_and_stops(monkeypatch, capsys):
    """A 500 on the list: friendly message, no input, no PATCH, token not shown."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    patch_calls = []

    def fake_patch(url, **kwargs):
        patch_calls.append(url)
        return FakeResponse(200, {})

    def fail_input(prompt=""):
        raise AssertionError("The script asked for input after a 500.")

    monkeypatch.setattr(
        requests, "get", lambda url, **kwargs: FakeResponse(500, "Server Error")
    )
    monkeypatch.setattr(requests, "patch", fake_patch)
    monkeypatch.setattr("builtins.input", fail_input)

    run_without_crashing()

    output = capsys.readouterr().out
    assert "The reading list API had a server error" in output
    assert "Django server terminal" in output
    assert FAKE_TOKEN not in output
    assert patch_calls == []
    assert "Before:" not in output
    assert "After:" not in output


def test_patch_500_shows_server_error_message_and_stops(monkeypatch, capsys):
    """A 500 on the PATCH: friendly message, no Before/After, token not shown."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    monkeypatch.setattr(
        requests, "get", lambda url, **kwargs: FakeResponse(200, TWO_BOOKS_PAGE)
    )
    monkeypatch.setattr(
        requests, "patch", lambda url, **kwargs: FakeResponse(500, "Server Error")
    )
    fake_inputs(monkeypatch, ["12", "finished"])

    run_without_crashing()

    output = capsys.readouterr().out
    assert "The reading list API had a server error" in output
    assert "Django server terminal" in output
    assert FAKE_TOKEN not in output
    assert "Before:" not in output
    assert "After:" not in output


# --- Timeouts: the API took longer than 10 seconds ---


def test_list_timeout_shows_message_and_stops(monkeypatch, capsys):
    """The list request times out: friendly message, no input, no PATCH."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    timeouts_used = []
    patch_calls = []

    def slow_get(url, **kwargs):
        timeouts_used.append(kwargs.get("timeout"))
        raise requests.Timeout("Read timed out.")

    def fake_patch(url, **kwargs):
        patch_calls.append(url)
        return FakeResponse(200, {})

    def fail_input(prompt=""):
        raise AssertionError("The script asked for input after a timeout.")

    monkeypatch.setattr(requests, "get", slow_get)
    monkeypatch.setattr(requests, "patch", fake_patch)
    monkeypatch.setattr("builtins.input", fail_input)

    run_without_crashing()

    output = capsys.readouterr().out
    assert "The API request timed out" in output
    assert "Django development server" in output
    assert FAKE_TOKEN not in output
    assert timeouts_used == [10]
    assert patch_calls == []
    assert "Before:" not in output
    assert "After:" not in output


def test_patch_timeout_shows_message_and_stops(monkeypatch, capsys):
    """The PATCH times out: friendly message, no Before/After, token not shown."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    timeouts_used = []

    def slow_patch(url, **kwargs):
        timeouts_used.append(kwargs.get("timeout"))
        raise requests.Timeout("Read timed out.")

    monkeypatch.setattr(
        requests, "get", lambda url, **kwargs: FakeResponse(200, TWO_BOOKS_PAGE)
    )
    monkeypatch.setattr(requests, "patch", slow_patch)
    fake_inputs(monkeypatch, ["12", "finished"])

    run_without_crashing()

    output = capsys.readouterr().out
    assert "The API request timed out" in output
    assert "Django development server" in output
    assert FAKE_TOKEN not in output
    assert timeouts_used == [10]
    assert "Before:" not in output
    assert "After:" not in output


# --- READING_LIST_API_URL overrides the default base URL ---


@pytest.mark.parametrize(
    ("url_setting", "expected_base"),
    [
        # Set: both requests use it.
        ("http://localhost:9000", "http://localhost:9000"),
        # Not set, or only spaces: the default local server.
        (None, "http://127.0.0.1:8000"),
        ("   ", "http://127.0.0.1:8000"),
        # Extra spaces and a trailing slash are cleaned up.
        ("  http://localhost:9000/  ", "http://localhost:9000"),
    ],
)
def test_api_url_setting_is_used_for_get_and_patch(
    monkeypatch, capsys, url_setting, expected_base
):
    """GET and PATCH both use READING_LIST_API_URL (or the default)."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    if url_setting is None:
        monkeypatch.delenv("READING_LIST_API_URL", raising=False)
    else:
        monkeypatch.setenv("READING_LIST_API_URL", url_setting)
    calls = []

    def fake_get(url, **kwargs):
        calls.append((url, kwargs))
        return FakeResponse(200, TWO_BOOKS_PAGE)

    def fake_patch(url, **kwargs):
        calls.append((url, kwargs))
        return FakeResponse(200, {"id": 12, "title": "Dune", "status": "finished"})

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(requests, "patch", fake_patch)
    fake_inputs(monkeypatch, ["12", "finished"])

    run_without_crashing()

    assert [url for url, _ in calls] == [
        f"{expected_base}/api/books/",
        f"{expected_base}/api/books/12/",
    ]
    for _, kwargs in calls:
        assert kwargs["headers"] == {"Authorization": f"Token {FAKE_TOKEN}"}
        assert kwargs["timeout"] == 10
    output = capsys.readouterr().out
    assert "After: finished" in output
    assert FAKE_TOKEN not in output


# --- A valid book ID that isn't on the first page ---


def test_book_not_on_first_page_shows_after_without_guessing_before(
    monkeypatch, capsys
):
    """PATCH works for book 99 (not listed), so Before is explained, not guessed."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    get_calls = []

    def fake_get(url, **kwargs):
        get_calls.append(url)
        return FakeResponse(200, TWO_BOOKS_PAGE)

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(
        requests,
        "patch",
        lambda url, **kwargs: FakeResponse(
            200, {"id": 99, "title": "Book on Page Two", "status": "finished"}
        ),
    )
    fake_inputs(monkeypatch, ["99", "finished"])

    try:
        api_script.main()
    except AttributeError as error:
        pytest.fail(f"The script crashed instead of showing a message: {error!r}")

    output = capsys.readouterr().out
    assert "Before: not available" in output
    assert "not on the first page" in output
    assert "After: finished" in output
    assert "Before: None" not in output
    # No extra request was made to look up the old status.
    assert len(get_calls) == 1


# --- Other HTTP 4xx errors: the API rejected the request ---


def test_list_403_shows_rejected_message_with_status_and_stops(monkeypatch, capsys):
    """An unexpected 4xx on the list: message with the code, no input, no PATCH."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    patch_calls = []

    def fake_patch(url, **kwargs):
        patch_calls.append(url)
        return FakeResponse(200, {})

    def fail_input(prompt=""):
        raise AssertionError("The script asked for input after a 403.")

    monkeypatch.setattr(
        requests,
        "get",
        lambda url, **kwargs: FakeResponse(403, {"detail": "Forbidden."}),
    )
    monkeypatch.setattr(requests, "patch", fake_patch)
    monkeypatch.setattr("builtins.input", fail_input)

    run_without_crashing()

    output = capsys.readouterr().out
    assert "The API rejected the request (HTTP 403)" in output
    assert FAKE_TOKEN not in output
    assert patch_calls == []
    assert "Before:" not in output
    assert "After:" not in output


def test_patch_400_shows_rejected_message_with_status_and_stops(monkeypatch, capsys):
    """An unexpected 4xx on the PATCH: message with the code, no Before/After."""
    monkeypatch.setenv("READING_LIST_TOKEN", FAKE_TOKEN)
    monkeypatch.setattr(
        requests, "get", lambda url, **kwargs: FakeResponse(200, TWO_BOOKS_PAGE)
    )
    monkeypatch.setattr(
        requests,
        "patch",
        lambda url, **kwargs: FakeResponse(400, {"status": ["Not a valid choice."]}),
    )
    fake_inputs(monkeypatch, ["12", "finished"])

    run_without_crashing()

    output = capsys.readouterr().out
    assert "The API rejected the request (HTTP 400)" in output
    assert FAKE_TOKEN not in output
    assert "Before:" not in output
    assert "After:" not in output
