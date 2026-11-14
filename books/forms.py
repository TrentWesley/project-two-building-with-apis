from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


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
