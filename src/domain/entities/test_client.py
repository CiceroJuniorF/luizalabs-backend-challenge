from src.domain.errors.domain_error import DomainError
from src.domain.entities.client import Client

NAME = "Fuu Bar"
EMAIL = "fuu.bar@mail.com"
EMPTY = ""
INVALID_EMAIL  = "invalid_email"

def test_should_create_client():
    client = Client(name=NAME, email=EMAIL)
    assert client.name == NAME and client.email == EMAIL

def test_shouldnt_create_client_without_name_and_email():
    try:
        Client(name=EMPTY, email=EMPTY)
    except Exception as e:
        assert isinstance(e, DomainError)
        assert str(e) == "Name is required, Email is required"

def test_shouldnt_create_client_with_invalid_email():
    try:
        Client(name=NAME, email=INVALID_EMAIL)
    except Exception as e:
        assert str(e) == "Invalid email"

def test_should_create_client_from_dict():
    client = Client.from_dict({"name": NAME, "email": EMAIL})
    assert client.name == NAME and client.email == EMAIL

def test_shouldnt_create_client_from_dict_without_name_and_email():
    try:
        Client.from_dict({"name": EMPTY, "email": EMPTY})
    except Exception as e:
        assert isinstance(e, DomainError)
        assert str(e) == "Name is required, Email is required"

def test_should_return_dict():
    client = Client(name=NAME, email=EMAIL)
    assert client.to_dict() == {"name": NAME, "email": EMAIL}