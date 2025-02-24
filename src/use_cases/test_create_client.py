
from src.domain.interfaces.id_generator import IdGenerator
from src.infra.repositories.memory.client_repository_memory  import ClientRepositoryMemory
from src.use_cases.create_client import CreateClient, CreateClientInput
from src.use_cases.errors.use_case_error import UseCaseError

NAME = "Fuu Bar"
EMAIL = "fuu.bar@mail.com"

class MockIdGenerator(IdGenerator):
    def generate(self) -> str:
        return "ABC123"

def __create_use_case(generator=MockIdGenerator(), repository=ClientRepositoryMemory()):
    return CreateClient(generator, repository)

def test_should_create_client():
    repository = ClientRepositoryMemory()
    create_client = __create_use_case(repository=repository)
    id = create_client.execute(CreateClientInput(name=NAME, email=EMAIL))
    client = repository.find_by_id(id)
    assert client.name == NAME and client.email == EMAIL

def test_shouldnt_create_client_already_exists():
    create_client = __create_use_case()
    id = create_client.execute(CreateClientInput(name=NAME, email=EMAIL))
    assert id == "ABC123"
    try:
        create_client.execute(CreateClientInput(name=NAME, email=EMAIL))
    except Exception as e:
        assert isinstance(e, UseCaseError)
        assert str(e) == "Client already exists"


