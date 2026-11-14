from datetime import UTC, datetime

import pytest
from django.contrib.auth.models import User

from books.models import SavedBook

TEST_PASSWORD = "Test-only-pass-2026!"


@pytest.mark.django_db
def test_reading_list_shows_only_the_logged_in_users_books(client):
    reader = User.objects.create_user(username="reader1", password=TEST_PASSWORD)
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    SavedBook.objects.create(
        user=reader, work_key="/works/OL893414W", title="Dune", author="Frank Herbert"
    )
    SavedBook.objects.create(
        user=other_reader,
        work_key="/works/OL27258W",
        title="Neuromancer",
        author="William Gibson",
    )
    client.force_login(reader)

    response = client.get("/books/")
    content = response.content.decode()

    assert response.status_code == 200
    assert "Dune" in content
    assert "Neuromancer" not in content


@pytest.fixture
def reader(db):
    return User.objects.create_user(username="reader1", password=TEST_PASSWORD)


def test_empty_reading_list_shows_friendly_message(client, reader):
    client.force_login(reader)

    response = client.get("/books/")

    assert "Your reading list is empty." in response.content.decode()


def test_reading_list_shows_newest_books_first(client, reader):
    first = SavedBook.objects.create(
        user=reader, work_key="/works/OL1W", title="First Saved", author="A"
    )
    second = SavedBook.objects.create(
        user=reader, work_key="/works/OL2W", title="Second Saved", author="B"
    )
    # Set clearly different save times so the order never depends on clock precision.
    SavedBook.objects.filter(pk=first.pk).update(
        created_at=datetime(2026, 1, 1, tzinfo=UTC)
    )
    SavedBook.objects.filter(pk=second.pk).update(
        created_at=datetime(2026, 2, 1, tzinfo=UTC)
    )
    client.force_login(reader)

    response = client.get("/books/")

    assert list(response.context["books"]) == [second, first]


def test_reading_list_card_shows_status_rating_and_cover(client, reader):
    SavedBook.objects.create(
        user=reader,
        work_key="/works/OL893414W",
        title="Dune",
        author="Frank Herbert",
        cover_id=11481354,
        status=SavedBook.Status.FINISHED,
        rating=4,
    )
    SavedBook.objects.create(
        user=reader, work_key="/works/OL2W", title="Coverless Book", author="B"
    )
    client.force_login(reader)

    content = client.get("/books/").content.decode()

    assert "Finished" in content
    assert "4 out of 5" in content
    assert "Not rated" in content
    assert "https://covers.openlibrary.org/b/id/11481354-M.jpg" in content
    assert "No cover" in content
