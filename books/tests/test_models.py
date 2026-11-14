import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from books.models import SavedBook

TEST_PASSWORD = "Test-only-pass-2026!"


def make_book(user, work_key="/works/OL893414W", title="Dune"):
    """Create a saved book with sensible test values."""
    return SavedBook.objects.create(
        user=user, work_key=work_key, title=title, author="Frank Herbert"
    )


@pytest.mark.django_db
def test_same_user_cannot_save_the_same_work_twice_but_another_user_can():
    reader = User.objects.create_user(username="reader1", password=TEST_PASSWORD)
    other_reader = User.objects.create_user(username="reader2", password=TEST_PASSWORD)
    make_book(reader)

    with pytest.raises(IntegrityError), transaction.atomic():
        make_book(reader)

    make_book(other_reader)
    assert SavedBook.objects.filter(work_key="/works/OL893414W").count() == 2


@pytest.mark.django_db
def test_rating_must_be_blank_or_between_1_and_5():
    reader = User.objects.create_user(username="reader1", password=TEST_PASSWORD)

    for bad_rating in [0, 6]:
        book = SavedBook(
            user=reader,
            work_key="/works/OL893414W",
            title="Dune",
            author="Frank Herbert",
            rating=bad_rating,
        )
        with pytest.raises(ValidationError) as error:
            book.full_clean()
        assert "rating" in error.value.message_dict

    for good_rating in [None, 1, 5]:
        book = SavedBook(
            user=reader,
            work_key="/works/OL893414W",
            title="Dune",
            author="Frank Herbert",
            rating=good_rating,
        )
        book.full_clean()  # raises ValidationError if the rating is rejected


@pytest.mark.django_db
def test_new_book_defaults_to_want_to_read_and_records_created_at():
    reader = User.objects.create_user(username="reader1", password=TEST_PASSWORD)

    book = make_book(reader)

    assert book.status == SavedBook.Status.WANT_TO_READ
    assert book.get_status_display() == "Want to Read"
    assert book.created_at is not None
    assert book.rating is None
    assert book.notes == ""


@pytest.mark.django_db
def test_deleting_a_user_deletes_their_saved_books():
    reader = User.objects.create_user(username="reader1", password=TEST_PASSWORD)
    make_book(reader)

    reader.delete()

    assert SavedBook.objects.count() == 0
