import pytest
from django.contrib.auth.models import User

from books.models import SavedBook

TEST_PASSWORD = "Test-only-pass-2026!"


@pytest.mark.django_db
def test_staff_can_search_saved_books_in_admin_by_username(client):
    admin_user = User.objects.create_superuser(
        username="admin1", password=TEST_PASSWORD
    )
    reader = User.objects.create_user(username="reader1", password=TEST_PASSWORD)
    SavedBook.objects.create(
        user=reader, work_key="/works/OL893414W", title="Dune", author="Frank Herbert"
    )
    client.force_login(admin_user)

    response = client.get("/admin/books/savedbook/?q=reader1")

    assert response.status_code == 200
    assert "Dune" in response.content.decode()


@pytest.mark.django_db
def test_regular_users_cannot_open_the_admin(client):
    reader = User.objects.create_user(username="reader1", password=TEST_PASSWORD)
    client.force_login(reader)

    response = client.get("/admin/books/savedbook/")

    assert response.status_code == 302
    assert "/admin/login/" in response.url
