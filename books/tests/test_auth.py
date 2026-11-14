import pytest
from django.contrib.auth import get_user
from django.contrib.auth.models import User

# A throwaway password used only inside tests.
TEST_PASSWORD = "Test-only-pass-2026!"


@pytest.mark.django_db
def test_signup_creates_user_logs_them_in_and_redirects_home(client):
    response = client.post(
        "/accounts/signup/",
        {"username": "reader1", "password1": TEST_PASSWORD, "password2": TEST_PASSWORD},
    )

    assert response.status_code == 302
    assert response.url == "/"
    assert User.objects.filter(username="reader1").exists()
    assert get_user(client).is_authenticated


@pytest.mark.django_db
def test_logout_requires_post_then_logs_out_and_redirects_home(client):
    user = User.objects.create_user(username="reader1", password=TEST_PASSWORD)
    client.force_login(user)

    get_response = client.get("/accounts/logout/")
    assert get_response.status_code == 405
    assert get_user(client).is_authenticated

    post_response = client.post("/accounts/logout/")
    assert post_response.status_code == 302
    assert post_response.url == "/"
    assert not get_user(client).is_authenticated


@pytest.fixture
def user(db):
    return User.objects.create_user(username="reader1", password=TEST_PASSWORD)


@pytest.mark.django_db
def test_signup_shows_welcome_message(client):
    response = client.post(
        "/accounts/signup/",
        {
            "username": "newreader",
            "password1": TEST_PASSWORD,
            "password2": TEST_PASSWORD,
        },
        follow=True,
    )

    assert "Welcome, newreader! Your account was created." in response.content.decode()


@pytest.mark.django_db
def test_signup_with_mismatched_passwords_shows_form_again(client):
    response = client.post(
        "/accounts/signup/",
        {
            "username": "newreader",
            "password1": TEST_PASSWORD,
            "password2": "Different-pass-2026!",
        },
    )

    assert response.status_code == 200
    assert not User.objects.filter(username="newreader").exists()
    assert not get_user(client).is_authenticated


def test_login_without_next_goes_to_reading_list(client, user):
    response = client.post(
        "/accounts/login/", {"username": "reader1", "password": TEST_PASSWORD}
    )

    assert response.status_code == 302
    assert response.url == "/books/"


def test_login_with_safe_next_goes_there(client, user):
    response = client.post(
        "/accounts/login/?next=/",
        {"username": "reader1", "password": TEST_PASSWORD, "next": "/"},
    )

    assert response.url == "/"


def test_login_ignores_unsafe_next(client, user):
    response = client.post(
        "/accounts/login/",
        {
            "username": "reader1",
            "password": TEST_PASSWORD,
            "next": "https://evil.example.com/",
        },
    )

    assert response.url == "/books/"


def test_failed_login_stays_on_page_with_error(client, user):
    response = client.post(
        "/accounts/login/", {"username": "reader1", "password": "wrong-password"}
    )

    assert response.status_code == 200
    assert "Please enter a correct username and password" in response.content.decode()
    assert not get_user(client).is_authenticated


def test_logout_shows_message(client, user):
    client.force_login(user)

    response = client.post("/accounts/logout/", follow=True)

    assert "You have been logged out." in response.content.decode()


@pytest.mark.parametrize("url", ["/accounts/login/", "/accounts/signup/"])
def test_logged_in_user_is_redirected_away_from_login_and_signup(client, user, url):
    client.force_login(user)

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == "/books/"
