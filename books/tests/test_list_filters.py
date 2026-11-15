import html
import re
from datetime import UTC, datetime
from urllib.parse import parse_qs, urlsplit

import pytest
from django.contrib.auth.models import User

from books.models import SavedBook

TEST_PASSWORD = "Test-only-pass-2026!"


@pytest.fixture
def reader(db):
    return User.objects.create_user(username="reader1", password=TEST_PASSWORD)


def add_book(user, number, title, author, **extra):
    """Save a book for this user with a unique, valid work key."""
    return SavedBook.objects.create(
        user=user, work_key=f"/works/OL{number}W", title=title, author=author, **extra
    )


def titles_on_page(response):
    return [book.title for book in response.context["books"]]


def test_search_matches_title_or_author_and_only_my_books(client, reader):
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    add_book(reader, 1, "The Left Hand of Darkness", "Ursula K. Le Guin")
    add_book(reader, 2, "Dune", "Frank Herbert")
    add_book(reader, 3, "Guinevere's Gift", "Nicole Carpenter")
    add_book(reader, 4, "Neuromancer", "William Gibson")
    add_book(other_reader, 5, "The Dispossessed", "Ursula K. Le Guin")
    client.force_login(reader)

    # Matches an author, ignoring capitals and surrounding spaces.
    by_author = client.get("/books/", {"q": "  LE GUIN  "})
    # Matches a title (part of a word, any capitalization).
    by_title = client.get("/books/", {"q": "guin"})

    assert titles_on_page(by_author) == ["The Left Hand of Darkness"]
    assert sorted(titles_on_page(by_title)) == [
        "Guinevere's Gift",
        "The Left Hand of Darkness",
    ]


@pytest.fixture
def three_books(reader):
    """Three of my books whose title, author, and date orders are all different.

    Newest first: Cloud Atlas, Anathem, Brave New World
    By title:     Anathem, Brave New World, Cloud Atlas
    By author:    Brave New World (Aldous), Cloud Atlas (David), Anathem (Neal)
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


NEWEST_FIRST = ["Cloud Atlas", "Anathem", "Brave New World"]


@pytest.mark.parametrize(
    ("params", "expected_titles"),
    [
        # Invalid or blank values are ignored: all my books, newest first.
        ({"status": "xyz"}, NEWEST_FIRST),
        ({"status": ""}, NEWEST_FIRST),
        ({"sort": "banana"}, NEWEST_FIRST),
        ({"sort": ""}, NEWEST_FIRST),
        ({}, NEWEST_FIRST),
        # Each valid status filters.
        ({"status": "want_to_read"}, ["Cloud Atlas"]),
        ({"status": "reading"}, ["Brave New World"]),
        ({"status": "finished"}, ["Anathem"]),
        # Each valid sort orders correctly.
        ({"sort": "newest"}, NEWEST_FIRST),
        ({"sort": "oldest"}, ["Brave New World", "Anathem", "Cloud Atlas"]),
        ({"sort": "title"}, ["Anathem", "Brave New World", "Cloud Atlas"]),
        ({"sort": "author"}, ["Brave New World", "Cloud Atlas", "Anathem"]),
    ],
    ids=[
        "invalid-status",
        "blank-status",
        "invalid-sort",
        "blank-sort",
        "no-params",
        "status-want-to-read",
        "status-reading",
        "status-finished",
        "sort-newest",
        "sort-oldest",
        "sort-title",
        "sort-author",
    ],
)
def test_status_and_sort_values_filter_and_order_safely(
    client, reader, three_books, params, expected_titles
):
    client.force_login(reader)

    response = client.get("/books/", params)

    assert response.status_code == 200
    assert titles_on_page(response) == expected_titles


def page_link_params(response, page_number):
    """The query parameters of the pagination link to `page_number`, as a dict."""
    content = response.content.decode()
    for href in re.findall(r'href="([^"]*)"', content):
        params = parse_qs(urlsplit(html.unescape(href)).query)
        if params.get("page") == [str(page_number)]:
            return {name: values[0] for name, values in params.items()}
    return None


def test_pagination_shows_10_per_page_and_keeps_filters(client, reader):
    # 13 of my books match q=saga AND status=reading: Saga 01 ... Saga 13.
    for number in range(1, 14):
        add_book(
            reader,
            number,
            f"Saga {number:02d}",
            "Some Author",
            status=SavedBook.Status.READING,
        )
    # Mine, but filtered out (wrong status, or no "saga" in the title or author).
    add_book(reader, 50, "Saga Finished", "Some Author", status="finished")
    add_book(reader, 51, "Unrelated Book", "Other Author", status="reading")
    # Another user's matching book: it would sort first by title if it leaked in.
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    add_book(other_reader, 99, "Saga 00", "Some Author", status="reading")
    client.force_login(reader)
    filters = {"q": "saga", "status": "reading", "sort": "title"}
    all_matches = [f"Saga {number:02d}" for number in range(1, 14)]

    page_1 = client.get("/books/", filters)

    # Filtering and sorting happen first, then 10 books per page.
    assert titles_on_page(page_1) == all_matches[:10]
    # The link to page 2 keeps the search, status, and sort.
    assert page_link_params(page_1, 2) == {**filters, "page": "2"}

    page_2 = client.get("/books/", {**filters, "page": "2"})

    # The rest are on page 2: nothing repeated, nothing missing.
    assert titles_on_page(page_2) == all_matches[10:]
    assert page_link_params(page_2, 1) == {**filters, "page": "1"}

    # Invalid page numbers show a real page instead of an error.
    not_a_number = client.get("/books/", {**filters, "page": "abc"})
    too_big = client.get("/books/", {**filters, "page": "999"})
    assert not_a_number.status_code == 200
    assert titles_on_page(not_a_number) == all_matches[:10]
    assert too_big.status_code == 200
    assert titles_on_page(too_big) == all_matches[10:]


# ---------------------------------------------------------------------------
# Other Phase 5 tests (normal tests, not /tdd)
# ---------------------------------------------------------------------------


def test_search_status_and_sort_work_together(client, reader):
    add_book(reader, 1, "Wizard of Earthsea", "Ursula K. Le Guin", status="finished")
    add_book(reader, 2, "The Lathe of Heaven", "Ursula K. Le Guin", status="finished")
    add_book(reader, 3, "The Dispossessed", "Ursula K. Le Guin", status="reading")
    add_book(reader, 4, "Dune", "Frank Herbert", status="finished")
    client.force_login(reader)

    response = client.get(
        "/books/", {"q": "le guin", "status": "finished", "sort": "title"}
    )

    assert titles_on_page(response) == ["The Lathe of Heaven", "Wizard of Earthsea"]


def test_status_counts_cover_my_whole_list_even_while_filtered(client, reader):
    add_book(reader, 1, "Book One", "A", status="want_to_read")
    add_book(reader, 2, "Book Two", "A", status="want_to_read")
    add_book(reader, 3, "Book Three", "A", status="reading")
    add_book(reader, 4, "Book Four", "A", status="finished")
    client.force_login(reader)
    expected = {"": 4, "want_to_read": 2, "reading": 1, "finished": 1}

    unfiltered = client.get("/books/")
    filtered = client.get("/books/", {"q": "four", "status": "finished"})

    for response in [unfiltered, filtered]:
        counts = {
            option["value"]: option["count"]
            for option in response.context["status_options"]
        }
        assert counts == expected
    assert titles_on_page(filtered) == ["Book Four"]


def test_status_counts_exclude_other_users_books(client, reader):
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    add_book(reader, 1, "Mine", "A", status="reading")
    add_book(other_reader, 2, "Theirs 1", "B", status="reading")
    add_book(other_reader, 3, "Theirs 2", "B", status="finished")
    client.force_login(reader)

    response = client.get("/books/")

    counts = {
        option["value"]: option["count"]
        for option in response.context["status_options"]
    }
    assert counts == {"": 1, "want_to_read": 0, "reading": 1, "finished": 0}


def test_no_matches_message_differs_from_empty_list_message(client, reader):
    client.force_login(reader)
    empty = client.get("/books/").content.decode()
    add_book(reader, 1, "Dune", "Frank Herbert")

    no_matches = client.get("/books/", {"q": "zzz-nothing"}).content.decode()

    assert "Your reading list is empty." in empty
    assert "No books match your filters." not in empty
    assert "No books match your filters." in no_matches
    assert "Your reading list is empty." not in no_matches


def test_sidebar_keeps_the_submitted_values(client, reader):
    add_book(reader, 1, "Dune", "Frank Herbert", status="reading")
    client.force_login(reader)

    content = client.get(
        "/books/", {"q": "  dune  ", "status": "reading", "sort": "author"}
    ).content.decode()

    assert 'action="/books/"' in content
    assert 'method="get"' in content
    assert 'name="q"' in content
    assert 'value="dune"' in content
    assert re.search(r'value="reading"\s+checked', content)
    assert re.search(r'value="author"\s+selected', content)
    assert ">Apply</button>" in content


def test_sidebar_shows_defaults_for_unknown_values(client, reader):
    add_book(reader, 1, "Dune", "Frank Herbert")
    client.force_login(reader)

    content = client.get(
        "/books/", {"status": "xyz", "sort": "banana"}
    ).content.decode()

    # "All" (value="") is selected, and the sort shows Newest saved.
    assert re.search(r'value=""\s+checked', content)
    assert re.search(r'value="newest"\s+selected', content)


def test_page_links_safely_encode_special_characters(client, reader):
    for number in range(1, 12):
        add_book(reader, number, f"Tom & Jerry {number:02d}", "Someone")
    client.force_login(reader)

    page_1 = client.get("/books/", {"q": "tom & jerry"})

    # The "&" in the search stays part of q instead of splitting the link.
    assert page_link_params(page_1, 2) == {"q": "tom & jerry", "page": "2"}


def test_list_shows_total_matching_books_not_just_this_page(client, reader):
    for number in range(1, 13):
        add_book(reader, number, f"Book {number:02d}", "Someone")
    client.force_login(reader)

    content = client.get("/books/").content.decode()

    assert "12 books" in content
    assert len(re.findall(r'class="card h-100', content)) == 10


def test_no_pagination_links_with_ten_or_fewer_books(client, reader):
    for number in range(1, 11):
        add_book(reader, number, f"Book {number:02d}", "Someone")
    client.force_login(reader)

    content = client.get("/books/").content.decode()

    assert 'aria-label="Reading list pages"' not in content
