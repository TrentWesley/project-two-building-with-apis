from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import RegexValidator

from .models import SavedBook


class BootstrapFormMixin:
    """Give every field Bootstrap's "form-control" style."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    """Django's built-in sign-up form, styled with Bootstrap."""


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    """Django's built-in login form, styled with Bootstrap."""


class SaveBookForm(forms.ModelForm):
    """Checks the hidden fields a search result's Save button submits.

    The owner (user) and status are never taken from the form; the view sets them.
    """

    # Only Open Library *work* keys are allowed, e.g. "/works/OL27448W".
    work_key = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                r"^/works/OL[0-9]+W$",
                message="Enter an Open Library work key like /works/OL27448W.",
            )
        ],
    )

    class Meta:
        model = SavedBook
        fields = ["work_key", "title", "author", "first_publish_year", "cover_id"]
