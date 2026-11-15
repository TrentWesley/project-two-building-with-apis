import re

import pytest
from django.contrib.auth.models import User

from books.models import SavedBook

TEST_PASSWORD = "Test-only-pass-2026!"


@pytest.fixture
def reader(db):
    return User.objects.create_user(username="reader1", password=TEST_PASSWORD)


def add_books(user, status, how_many, first_number):
    """Save `how_many` books with this status, using unique work keys."""
    for number in range(first_number, first_number + how_many):
        SavedBook.objects.create(
            user=user,
            work_key=f"/works/OL{number}W",
            title=f"Book {number}",
            author="Someone",
            status=status,
        )


def shown_count(content, name):
    """The number the home page shows in the count box with id="count-<name>"."""
    match = re.search(rf'id="count-{name}"[^>]*>\s*(\d+)\s*<', content)
    if match is None:
        return None
    return int(match.group(1))


def test_logged_in_home_shows_my_status_counts(client, reader):
    add_books(reader, SavedBook.Status.WANT_TO_READ, 3, first_number=1)
    add_books(reader, SavedBook.Status.READING, 2, first_number=10)
    add_books(reader, SavedBook.Status.FINISHED, 1, first_number=20)
    client.force_login(reader)

    content = client.get("/").content.decode()

    assert shown_count(content, "want_to_read") == 3
    assert shown_count(content, "reading") == 2
    assert shown_count(content, "finished") == 1
    assert shown_count(content, "all") == 6


def displayed_counts(client):
    """All four numbers the home page shows, read from the HTML."""
    content = client.get("/").content.decode()
    names = ["want_to_read", "reading", "finished", "all"]
    return {name: shown_count(content, name) for name in names}


def test_home_counts_exclude_other_users_books(client, reader):
    """Regression test: behavior 1's view already counts only the logged-in
    user's books, so this test passed on its first run (no RED)."""
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    # reader1: 1 want to read, 2 reading, 0 finished (3 total)
    add_books(reader, SavedBook.Status.WANT_TO_READ, 1, first_number=1)
    add_books(reader, SavedBook.Status.READING, 2, first_number=10)
    # reader2: 4 want to read, 0 reading, 3 finished (7 total)
    add_books(other_reader, SavedBook.Status.WANT_TO_READ, 4, first_number=30)
    add_books(other_reader, SavedBook.Status.FINISHED, 3, first_number=40)

    client.force_login(reader)
    reader1_counts = displayed_counts(client)
    client.force_login(other_reader)
    reader2_counts = displayed_counts(client)

    assert reader1_counts == {"want_to_read": 1, "reading": 2, "finished": 0, "all": 3}
    assert reader2_counts == {"want_to_read": 4, "reading": 0, "finished": 3, "all": 7}


def test_logged_out_home_is_public_and_shows_no_private_counts(client, reader):
    """Regression test: the counts were added only inside the logged-in part of
    the page (behavior 1), so this test passed on its first run (no RED)."""
    add_books(reader, SavedBook.Status.READING, 2, first_number=1)
    SavedBook.objects.create(
        user=reader, work_key="/works/OL99W", title="Secret Diary Book", author="Hidden"
    )

    response = client.get("/")  # not logged in
    content = response.content.decode()

    assert response.status_code == 200
    # The public introduction and the account buttons.
    assert "Your personal reading list" in content
    assert 'href="/accounts/signup/"' in content
    assert ">Sign Up</a>" in content
    assert 'href="/accounts/login/"' in content
    assert ">Log In</a>" in content
    # No count boxes at all...
    for name in ["want_to_read", "reading", "finished", "all"]:
        assert shown_count(content, name) is None
        assert f'id="count-{name}"' not in content
    # ...and nothing about the user or their books.
    assert "Welcome back" not in content
    assert "reader1" not in content
    assert "Secret Diary Book" not in content
    assert "Book 1" not in content


# ---------------------------------------------------------------------------
# Other Phase 7 tests (normal tests, not /tdd)
# ---------------------------------------------------------------------------

# Typed directly in the template, so the apostrophe is not HTML-escaped.
EMPTY_MESSAGE = "You haven't saved any books yet."


def test_new_user_sees_zero_counts_and_a_friendly_message(client, reader):
    client.force_login(reader)

    content = client.get("/").content.decode()

    assert displayed_counts(client) == {
        "want_to_read": 0,
        "reading": 0,
        "finished": 0,
        "all": 0,
    }
    assert EMPTY_MESSAGE in content
    assert "Search Open Library to get started." in content


def test_friendly_message_is_hidden_once_a_book_is_saved(client, reader):
    add_books(reader, SavedBook.Status.FINISHED, 1, first_number=1)
    client.force_login(reader)

    content = client.get("/").content.decode()

    assert EMPTY_MESSAGE not in content
    assert shown_count(content, "all") == 1


def test_friendly_message_ignores_other_users_books(client, reader):
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    add_books(other_reader, SavedBook.Status.READING, 2, first_number=1)
    client.force_login(reader)

    content = client.get("/").content.decode()

    assert EMPTY_MESSAGE in content


def test_logged_in_home_links_to_search_and_reading_list(client, reader):
    client.force_login(reader)

    content = client.get("/").content.decode()

    assert 'href="/search/">Search Books</a>' in content
    assert 'href="/books/">My Reading List</a>' in content
    assert "Welcome back, reader1!" in content
    # The visitor buttons are not shown to logged-in users.
    assert ">Sign Up</a>" not in content
