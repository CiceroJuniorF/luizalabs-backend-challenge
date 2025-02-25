
from dataclasses import dataclass
from src.domain.entities.client import Client
from src.domain.interfaces.id_generator import IdGenerator
from src.domain.interfaces.repositories.client_repository import ClientRepository
from src.use_cases.errors.use_case_error import UseCaseError

@dataclass
class CreateClientInput:
    name: str
    email: str

class CreateClient:
    def __init__(self, id_gen: IdGenerator, client_repo: ClientRepository):
        self.client_repo = client_repo
        self.id_gen = id_gen

    def execute(self, input: CreateClientInput) -> str:
        '''
        Creates a new client if not exists
        :param input: CreateClientInput
        return ID: str
        '''
        if(self.client_repo.email_exists(input.email)):
            raise UseCaseError("Client already exists")
        ID = self.id_gen.generate()
        client = Client(id=ID, name=input.name, email=input.email)
        self.client_repo.save(client=client)
        return ID