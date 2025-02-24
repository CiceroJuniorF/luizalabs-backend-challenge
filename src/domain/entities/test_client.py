from src.domain.errors.domain_error import DomainError
from src.domain.entities.client import Client
from src.domain.interfaces.id_generator import IdGenerator

NAME = "Fuu Bar"
EMAIL = "fuu.bar@mail.com"
EMPTY = ""
INVALID_EMAIL  = "invalid_email"

class MockIdGenerator(IdGenerator):
    def generate(self) -> str:
        return "ABC123"

id = MockIdGenerator()
ID = id.generate()

def test_should_create_client():
    client = Client(id=ID, name=NAME, email=EMAIL)
    assert client.id == ID and client.name == NAME and client.email == EMAIL

def test_shouldnt_create_client_with_all_fields_empty():
    try:
        Client(id=EMPTY, name=EMPTY, email=EMPTY)
    except Exception as e:
        assert isinstance(e, DomainError)
        assert str(e) == "Id is required, Name is required, Email is required"

def test_shouldnt_create_client_with_invalid_email():
    try:
        Client(id=ID, name=NAME, email=INVALID_EMAIL)
    except Exception as e:
        assert str(e) == "Invalid email"

def test_should_create_client_from_dict():
    client = Client.from_dict({"id":ID, "name": NAME, "email": EMAIL})
    assert client.name == NAME and client.email == EMAIL

def test_shouldnt_create_client_from_dict_with_all_fields_empty():
    try:
        Client.from_dict({"id":EMPTY, "name": EMPTY, "email": EMPTY})
    except Exception as e:
        assert isinstance(e, DomainError)
        assert str(e) == "Id is required, Name is required, Email is required"

def test_should_return_dict():
    client = Client(id=ID, name=NAME, email=EMAIL)
    assert client.to_dict() == {"id":ID, "name": NAME, "email": EMAIL}