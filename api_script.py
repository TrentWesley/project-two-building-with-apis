"""Script 2: list my saved books through our reading list API and update one status.

Run the Django server first, then: uv run api_script.py
"""

import os

import requests

DEFAULT_API_URL = "http://127.0.0.1:8000"
TIMEOUT_SECONDS = 10
STATUSES = ["want_to_read", "reading", "finished"]

MISSING_TOKEN_MESSAGE = (
    "READING_LIST_TOKEN is not set.\n"
    "Create a token with: uv run manage.py drf_create_token <your-username>\n"
    "Then set it in this terminal (not in a file) and run the script again."
)

EMPTY_LIST_MESSAGE = (
    "Your reading list is empty.\n"
    "Search for a book on the website (/search/) and save it, then run this script again."
)

SERVER_ERROR_MESSAGE = (
    "The reading list API had a server error.\n"
    "Check the Django server terminal for details, then try again."
)

TOKEN_REJECTED_MESSAGE = (
    "Your API token was rejected (HTTP 401).\n"
    "Check that READING_LIST_TOKEN is set to your current token, or create one with:\n"
    "uv run manage.py drf_create_token <your-username>"
)


def get_token():
    """The API token from the READING_LIST_TOKEN environment variable ("" if unset)."""
    return os.environ.get("READING_LIST_TOKEN", "").strip()


def get_api_url():
    """The API's base URL from READING_LIST_API_URL, or the local default.

    Spaces and a trailing slash are removed, so "http://localhost:9000/ "
    becomes "http://localhost:9000".
    """
    url = os.environ.get("READING_LIST_API_URL", "").strip().rstrip("/")
    if not url:
        return DEFAULT_API_URL
    return url


def auth_headers(token):
    """The header that logs in to our API with a token."""
    return {"Authorization": f"Token {token}"}


def list_books(base_url, token):
    """Get the first page of my saved books and return its list of books."""
    response = requests.get(
        f"{base_url}/api/books/",
        headers=auth_headers(token),
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json().get("results", [])


def update_status(base_url, token, book_id, status):
    """Change one book's status with PATCH and return the updated book."""
    response = requests.patch(
        f"{base_url}/api/books/{book_id}/",
        json={"status": status},
        headers=auth_headers(token),
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def format_book(book):
    """One book as a display line, for example: [12] Dune - want_to_read"""
    book_id = book.get("id", "?")
    title = book.get("title", "Unknown title")
    status = book.get("status", "unknown")
    return f"[{book_id}] {title} - {status}"


def cannot_reach_message(base_url):
    """The message shown when the Django server can't be reached."""
    return (
        f"Could not reach the reading list API at {base_url}.\n"
        "Check that the Django development server is running "
        "(uv run manage.py runserver) and try again."
    )


def timed_out_message(base_url):
    """The message shown when the API takes longer than TIMEOUT_SECONDS to answer."""
    return (
        f"The API request timed out after {TIMEOUT_SECONDS} seconds ({base_url}).\n"
        "Check that the Django development server is running and responding, "
        "then try again."
    )


def invalid_response_message(base_url):
    """The message shown when the API's answer can't be read as JSON."""
    return (
        "The API returned an invalid response (not JSON).\n"
        f"Check that the reading list server is running at {base_url} and try again."
    )


def http_status(error):
    """The HTTP status code inside a requests HTTPError (None if there isn't one)."""
    if error.response is None:
        return None
    return error.response.status_code


def is_server_error(error):
    """True if the HTTPError is a server error (status 500 or higher)."""
    status = http_status(error)
    return status is not None and status >= 500


def rejected_message(error):
    """The message for an HTTP error with no more specific message (for example, 403)."""
    return (
        f"The API rejected the request (HTTP {http_status(error)}).\n"
        "Check your input and token, then try again."
    )


def book_id_error(book_id):
    """A message explaining what's wrong with the typed book ID, or "" if it's fine."""
    if not book_id:
        return "Please enter a book ID."
    if not book_id.isdigit():
        return f'"{book_id}" is not a valid book ID. Enter a number, like 12.'
    return ""


def status_error(status):
    """A message explaining what's wrong with the typed status, or "" if it's fine."""
    choices = ", ".join(STATUSES)
    if not status:
        return f"Please enter a status. Choose one of: {choices}"
    if status not in STATUSES:
        return f'"{status}" is not a valid status. Choose one of: {choices}'
    return ""


def find_book(books, book_id):
    """The book in `books` with this ID (a string from input), or None."""
    for book in books:
        if str(book.get("id")) == book_id:
            return book
    return None


def main():
    """List my books, ask for a book ID and a new status, and update it."""
    token = get_token()
    if not token:
        print(MISSING_TOKEN_MESSAGE)
        return

    base_url = get_api_url()
    try:
        books = list_books(base_url, token)
    except requests.Timeout:
        # Checked first: a connect timeout is both a Timeout and a ConnectionError.
        print(timed_out_message(base_url))
        return
    except requests.ConnectionError:
        print(cannot_reach_message(base_url))
        return
    except requests.HTTPError as error:
        if http_status(error) == 401:
            print(TOKEN_REJECTED_MESSAGE)
            return
        if is_server_error(error):
            print(SERVER_ERROR_MESSAGE)
            return
        # Any other HTTP error (for example, 403).
        print(rejected_message(error))
        return
    except ValueError:
        # The response body wasn't JSON (requests.JSONDecodeError is a ValueError).
        print(invalid_response_message(base_url))
        return

    if not books:
        print(EMPTY_LIST_MESSAGE)
        return

    print("Your saved books (Showing the first page only):")
    for book in books:
        print(format_book(book))
    print()

    # Check each answer before sending anything to the API.
    book_id = input("Book ID to update: ").strip()
    error = book_id_error(book_id)
    if error:
        print(error)
        return

    new_status = input("New status (want_to_read, reading, finished): ").strip()
    error = status_error(new_status)
    if error:
        print(error)
        return

    before = find_book(books, book_id)
    try:
        updated = update_status(base_url, token, book_id, new_status)
    except requests.Timeout:
        # Checked first: a connect timeout is both a Timeout and a ConnectionError.
        print(timed_out_message(base_url))
        return
    except requests.ConnectionError:
        print(cannot_reach_message(base_url))
        return
    except requests.HTTPError as error:
        if http_status(error) == 401:
            print(TOKEN_REJECTED_MESSAGE)
            return
        # 404 means the book doesn't exist or belongs to someone else.
        if http_status(error) == 404:
            print(f"No book with ID {book_id} in your reading list.")
            return
        if is_server_error(error):
            print(SERVER_ERROR_MESSAGE)
            return
        # Any other HTTP error (for example, 400).
        print(rejected_message(error))
        return
    except ValueError:
        print(invalid_response_message(base_url))
        return

    if before is None:
        # The book exists (the PATCH worked) but wasn't in the list we showed,
        # so we don't know its old status. Say so instead of guessing.
        print(
            f"Before: not available (book {book_id} is not on the first page shown above)"
        )
    else:
        print(f"Before: {before.get('status')}")
    print(f"After: {updated.get('status')}")


if __name__ == "__main__":
    main()
