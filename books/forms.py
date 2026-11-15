from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import RegexValidator

from .models import SavedBook


class BootstrapFormMixin:
    """Give every field Bootstrap's style ("form-select" for dropdowns)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
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


class EditBookForm(BootstrapFormMixin, forms.ModelForm):
    """Edit a saved book's reading information.

    Only these three fields are on the form, so any other submitted value
    (title, author, work key, year, cover, or owner) is ignored.
    """

    class Meta:
        model = SavedBook
        fields = ["status", "rating", "notes"]
        labels = {"status": "Reading status", "rating": "Rating (1–5)"}
        help_texts = {
            "rating": "Optional. 1 is the lowest and 5 is the highest.",
            "notes": "Optional.",
        }
        widgets = {
            # min/max help the browser; the model's 1–5 validators are the real rule.
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }
