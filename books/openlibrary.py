"""The only place the reading list app talks to the Open Library API."""

import requests

SEARCH_URL = "https://openlibrary.org/search.json"
USER_AGENT = "CIDM3312-BookSearch/1.0"
RESULT_LIMIT = 10
TIMEOUT_SECONDS = 10


class OpenLibraryError(Exception):
    """Open Library could not be reached or sent back something unusable."""


def search_books(title):
    """Search Open Library by title.

    Returns {"total": <number of matches>, "books": [<clean book dictionaries>]}.
    Raises OpenLibraryError for any network, HTTP, or response problem.
    """
    try:
        response = requests.get(
            SEARCH_URL,
            params={
                "title": title,
                "fields": "key,title,author_name,first_publish_year,cover_i",
                "limit": RESULT_LIMIT,
            },
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.exceptions.RequestException, ValueError) as error:
        raise OpenLibraryError(str(error)) from error

    if not isinstance(data, dict):
        raise OpenLibraryError("Open Library sent an unexpected response.")

    docs = data.get("docs", [])
    return {
        "total": data.get("numFound", 0),
        "books": [clean_book(doc) for doc in docs],
    }


def clean_book(doc):
    """Turn one raw Open Library search result into a tidy dictionary.

    The keys match the SavedBook model's field names, so a result can be saved later.
    """
    author_names = doc.get("author_name", [])
    if author_names:
        author = ", ".join(author_names)
    else:
        author = "Unknown author"

    return {
        "work_key": doc.get("key", ""),
        "title": doc.get("title", "Unknown title"),
        "author": author,
        "first_publish_year": doc.get("first_publish_year"),
        "cover_id": doc.get("cover_i"),
    }
