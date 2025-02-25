
from src.domain.interfaces.id_generator import IdGenerator
from src.infra.repositories.memory.customer_repository_memory  import CustomerRepositoryMemory
from src.use_cases.create_customer import CreateCustomer, CreateCustomerInput
from src.use_cases.errors.use_case_error import UseCaseError

NAME = "Fuu Bar"
EMAIL = "fuu.bar@mail.com"

class MockIdGenerator(IdGenerator):
    def generate(self) -> str:
        return "ABC123"

def __create_use_case(generator=MockIdGenerator(), repository=CustomerRepositoryMemory()):
    return CreateCustomer(generator, repository)

def test_should_create_customer():
    repository = CustomerRepositoryMemory()
    create_customer = __create_use_case(repository=repository)
    id = create_customer.execute(CreateCustomerInput(name=NAME, email=EMAIL))
    customer = repository.find_by_id(id)
    assert customer.name == NAME and customer.email == EMAIL

def test_shouldnt_create_customer_already_exists():
    create_customer = __create_use_case()
    id = create_customer.execute(CreateCustomerInput(name=NAME, email=EMAIL))
    assert id == "ABC123"
    try:
        create_customer.execute(CreateCustomerInput(name=NAME, email=EMAIL))
    except Exception as e:
        assert isinstance(e, UseCaseError)
        assert str(e) == "Customer already exists"


