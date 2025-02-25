
from dataclasses import dataclass
from src.application.errors.application_errors_enum import ApplicationErrors
from src.domain.entities.customer import Customer
from src.domain.interfaces.id_generator import IdGenerator
from src.domain.interfaces.repositories.customer_repository import CustomerRepository
from src.application.errors.application_error import ApplicationError

@dataclass
class CreateCustomerInput:
    name: str
    email: str
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class CreateCustomer:
    def __init__(self, id_gen: IdGenerator, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo
        self.id_gen = id_gen

    async def execute(self, input: CreateCustomerInput) -> str:
        '''
        Creates a new Customer if not exists
        :param input: CreateCustomerInput
        return ID: str
        '''
        if(self.customer_repo.email_exists(input.email)):
            raise ApplicationError(ApplicationErrors.CONFLICT, "Customer already exists")
        customer = Customer(id=self.id_gen.generate(), name=input.name, email=input.email)
        ID = self.customer_repo.save(customer=customer)
        return ID