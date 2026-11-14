import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_home_shows_intro_and_buttons_to_anonymous_visitors(client):
    response = client.get("/")
    content = response.content.decode()

    assert response.status_code == 200
    assert "Sign Up" in content
    assert "Log In" in content


@pytest.mark.django_db
def test_home_welcomes_logged_in_user(client):
    user = User.objects.create_user(username="reader1", password="Test-only-pass-2026!")
    client.force_login(user)

    response = client.get("/")

    assert "Welcome back, reader1!" in response.content.decode()


@pytest.mark.django_db
def test_reading_list_redirects_anonymous_user_to_login_with_next(client):
    response = client.get("/books/")

    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/books/"


@pytest.mark.django_db
def test_reading_list_placeholder_loads_for_logged_in_user(client):
    user = User.objects.create_user(username="reader1", password="Test-only-pass-2026!")
    client.force_login(user)

    response = client.get("/books/")

    assert response.status_code == 200
    assert "My Reading List" in response.content.decode()


@pytest.mark.django_db
def test_signup_and_login_pages_load_for_anonymous_visitors(client):
    assert client.get("/accounts/signup/").status_code == 200
    assert client.get("/accounts/login/").status_code == 200
