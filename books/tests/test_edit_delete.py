import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from books.models import SavedBook

TEST_PASSWORD = "Test-only-pass-2026!"


@pytest.fixture
def reader(db):
    return User.objects.create_user(username="reader1", password=TEST_PASSWORD)


@pytest.fixture
def dune(reader):
    """One of reader1's saved books, with every Open Library field filled in."""
    return SavedBook.objects.create(
        user=reader,
        work_key="/works/OL893414W",
        title="Dune",
        author="Frank Herbert",
        first_publish_year=1965,
        cover_id=11481354,
    )


def test_editing_changes_only_status_rating_and_notes(client, reader, dune):
    someone_else = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    client.force_login(reader)

    response = client.post(
        f"/books/{dune.pk}/edit/",
        {
            # The three fields the user may change.
            "status": "reading",
            "rating": "4",
            "notes": "Loving the desert planet.",
            # Tampered values (e.g. added in developer tools) must be ignored.
            "title": "Hacked Title",
            "author": "Hacker",
            "work_key": "/works/OL1W",
            "first_publish_year": "1900",
            "cover_id": "1",
            "user": someone_else.pk,
        },
    )

    dune.refresh_from_db()
    # The user's own information was saved...
    assert dune.status == SavedBook.Status.READING
    assert dune.rating == 4
    assert dune.notes == "Loving the desert planet."
    # ...and Open Library's facts and the owner did not change.
    assert dune.title == "Dune"
    assert dune.author == "Frank Herbert"
    assert dune.work_key == "/works/OL893414W"
    assert dune.first_publish_year == 1965
    assert dune.cover_id == 11481354
    assert dune.user == reader
    assert response.status_code == 302
    assert response.url == "/books/"


@pytest.fixture
def other_readers_book(db):
    """A book saved by a different user (reader2)."""
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    return SavedBook.objects.create(
        user=other_reader,
        work_key="/works/OL27258W",
        title="Neuromancer",
        author="William Gibson",
        status=SavedBook.Status.WANT_TO_READ,
    )


# What a tampering POST would try to set.
HACKED_EDIT = {"status": "finished", "rating": "1", "notes": "Hacked"}


@pytest.mark.parametrize("action", ["edit", "delete"])
@pytest.mark.parametrize("method", ["get", "post"])
def test_another_users_book_returns_404_and_is_not_changed(
    client, reader, dune, other_readers_book, action, method
):
    client.force_login(reader)
    their_url = f"/books/{other_readers_book.pk}/{action}/"

    if method == "post":
        response = client.post(their_url, HACKED_EDIT)
    else:
        response = client.get(their_url)

    assert response.status_code == 404
    # Their book still exists, completely unchanged.
    their_book = SavedBook.objects.get(pk=other_readers_book.pk)
    assert their_book.status == SavedBook.Status.WANT_TO_READ
    assert their_book.rating is None
    assert their_book.notes == ""
    # Control: the same kind of page works for my own book, so the 404 above
    # comes from the ownership rule, not from a missing page.
    assert client.get(f"/books/{dune.pk}/{action}/").status_code == 200


@pytest.mark.parametrize("action", ["edit", "delete"])
@pytest.mark.parametrize("method", ["get", "post"])
def test_logged_out_users_are_sent_to_login(client, dune, action, method):
    url = f"/books/{dune.pk}/{action}/"

    if method == "post":
        response = client.post(url, HACKED_EDIT)
    else:
        response = client.get(url)

    assert response.status_code == 302
    assert response.url == f"/accounts/login/?next={url}"
    dune.refresh_from_db()
    assert dune.status == SavedBook.Status.WANT_TO_READ


def test_get_only_shows_confirmation_and_post_deletes(client, reader, dune):
    """Regression test: Django's DeleteView already provided this when behavior 2
    added the delete page, so this test passed on its first run (no RED)."""
    client.force_login(reader)
    url = f"/books/{dune.pk}/delete/"

    confirmation = client.get(url)

    # GET only shows the question, with a POST form protected by CSRF.
    content = confirmation.content.decode()
    assert confirmation.status_code == 200
    assert "Remove <strong>Dune</strong> from your reading list?" in content
    assert 'method="post"' in content
    assert 'name="csrfmiddlewaretoken"' in content
    # ...and the book is still there, unchanged.
    dune.refresh_from_db()
    assert dune.title == "Dune"
    assert dune.status == SavedBook.Status.WANT_TO_READ

    response = client.post(url)

    assert response.status_code == 302
    assert response.url == "/books/"
    assert not SavedBook.objects.filter(pk=dune.pk).exists()


# ---------------------------------------------------------------------------
# Other Phase 6 tests (normal tests, not /tdd)
# ---------------------------------------------------------------------------


def message_texts(response):
    """The messages Django queued for the next page."""
    return [str(message) for message in get_messages(response.wsgi_request)]


@pytest.mark.parametrize("bad_rating", ["0", "6", "-1", "five"])
def test_invalid_rating_shows_error_and_changes_nothing(
    client, reader, dune, bad_rating
):
    client.force_login(reader)

    response = client.post(
        f"/books/{dune.pk}/edit/",
        {"status": "finished", "rating": bad_rating, "notes": "Should not save"},
    )

    # The form comes back (no redirect) with an error on the rating field.
    assert response.status_code == 200
    assert "rating" in response.context["form"].errors
    assert "Please fix the errors below." in response.content.decode()
    dune.refresh_from_db()
    assert dune.status == SavedBook.Status.WANT_TO_READ
    assert dune.rating is None
    assert dune.notes == ""


def test_invalid_status_shows_error_and_changes_nothing(client, reader, dune):
    client.force_login(reader)

    response = client.post(
        f"/books/{dune.pk}/edit/", {"status": "lost", "rating": "3", "notes": ""}
    )

    assert response.status_code == 200
    assert "status" in response.context["form"].errors
    dune.refresh_from_db()
    assert dune.status == SavedBook.Status.WANT_TO_READ
    assert dune.rating is None


@pytest.mark.parametrize("good_rating", ["1", "5"])
def test_ratings_1_and_5_are_allowed(client, reader, dune, good_rating):
    client.force_login(reader)

    client.post(
        f"/books/{dune.pk}/edit/", {"status": "finished", "rating": good_rating}
    )

    dune.refresh_from_db()
    assert dune.rating == int(good_rating)


def test_rating_and_notes_are_optional_and_can_be_cleared(client, reader, dune):
    SavedBook.objects.filter(pk=dune.pk).update(rating=4, notes="Old notes")
    client.force_login(reader)

    response = client.post(
        f"/books/{dune.pk}/edit/", {"status": "reading", "rating": "", "notes": ""}
    )

    assert response.status_code == 302
    dune.refresh_from_db()
    assert dune.status == SavedBook.Status.READING
    assert dune.rating is None
    assert dune.notes == ""


def test_edit_shows_success_message(client, reader, dune):
    client.force_login(reader)

    response = client.post(f"/books/{dune.pk}/edit/", {"status": "reading"})

    assert "Updated Dune." in message_texts(response)


def test_delete_shows_success_message(client, reader, dune):
    client.force_login(reader)

    response = client.post(f"/books/{dune.pk}/delete/")

    assert response.url == "/books/"
    assert "Removed Dune." in message_texts(response)


def test_reading_list_cards_link_to_edit_and_delete(client, reader, dune):
    client.force_login(reader)

    content = client.get("/books/").content.decode()

    assert f'href="/books/{dune.pk}/edit/"' in content
    assert f'href="/books/{dune.pk}/delete/"' in content


def test_edit_page_shows_book_info_read_only_and_only_three_fields(
    client, reader, dune
):
    client.force_login(reader)

    response = client.get(f"/books/{dune.pk}/edit/")
    content = response.content.decode()

    # The book's facts are shown...
    assert "Dune" in content
    assert "Frank Herbert" in content
    assert "First published 1965" in content
    assert "https://covers.openlibrary.org/b/id/11481354-M.jpg" in content
    # ...but the form only has the three editable fields.
    assert list(response.context["form"].fields) == ["status", "rating", "notes"]
    for read_only in ["title", "author", "work_key", "first_publish_year", "cover_id"]:
        assert f'name="{read_only}"' not in content


def test_edit_form_starts_with_the_current_values(client, reader, dune):
    SavedBook.objects.filter(pk=dune.pk).update(
        status="finished", rating=5, notes="A classic."
    )
    client.force_login(reader)

    content = client.get(f"/books/{dune.pk}/edit/").content.decode()

    assert '<option value="finished" selected>' in content
    assert 'value="5"' in content
    assert "A classic.</textarea>" in content


def test_delete_page_shows_book_info_and_cancel_link(client, reader, dune):
    client.force_login(reader)

    content = client.get(f"/books/{dune.pk}/delete/").content.decode()

    assert "Frank Herbert" in content
    assert "https://covers.openlibrary.org/b/id/11481354-M.jpg" in content
    assert 'href="/books/" class="btn btn-outline-secondary">Cancel</a>' in content
    assert SavedBook.objects.filter(pk=dune.pk).exists()


@pytest.mark.parametrize("action", ["edit", "delete"])
def test_missing_book_id_returns_404(client, reader, action):
    client.force_login(reader)

    response = client.get(f"/books/99999/{action}/")

    assert response.status_code == 404
