import pytest
import requests


@pytest.fixture(autouse=True)
def block_real_network(monkeypatch):
    """Fail loudly if any test tries to call a real website.

    Tests that need HTTP replace requests.get with their own fake.
    """

    def refuse_network(*args, **kwargs):
        raise RuntimeError("A test tried to make a real network request.")

    monkeypatch.setattr(requests, "get", refuse_network)
