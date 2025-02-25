from src.domain.errors.domain_error import DomainError
from src.domain.entities.customer import Customer
from src.domain.interfaces.id_generator import IdGenerator

NAME = "Fuu Bar"
EMAIL = "fuu.bar@mail.com"
EMPTY = ""
INVALID_EMAIL  = "invalid_email"

class MockIdGenerator(IdGenerator):
    def generate(self) -> str:
        return "ABC123"

generator = MockIdGenerator()
ID = generator.generate()

def test_should_create_customer():
    customer = Customer(id=ID, name=NAME, email=EMAIL)
    assert customer.id == ID and customer.name == NAME and customer.email == EMAIL

def test_shouldnt_create_customer_with_all_fields_empty():
    try:
        Customer(id=EMPTY, name=EMPTY, email=EMPTY)
    except Exception as e:
        assert isinstance(e, DomainError)
        assert str(e) == "Id is required, Name is required, Email is required"

def test_shouldnt_create_customer_with_invalid_email():
    try:
        Customer(id=ID, name=NAME, email=INVALID_EMAIL)
    except Exception as e:
        assert str(e) == "Invalid email"

def test_should_create_customer_from_dict():
    customer = Customer.from_dict({"id":ID, "name": NAME, "email": EMAIL})
    assert customer.name == NAME and customer.email == EMAIL

def test_shouldnt_create_customer_from_dict_with_all_fields_empty():
    try:
        Customer.from_dict({"id":EMPTY, "name": EMPTY, "email": EMPTY})
    except Exception as e:
        assert isinstance(e, DomainError)
        assert str(e) == "Id is required, Name is required, Email is required"

def test_should_return_dict():
    customer = Customer(id=ID, name=NAME, email=EMAIL)
    assert customer.to_dict() == {"id":ID, "name": NAME, "email": EMAIL}