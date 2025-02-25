
from dataclasses import dataclass
from src.domain.entities.customer import Customer
from src.domain.interfaces.id_generator import IdGenerator
from src.domain.interfaces.repositories.customer_repository import CustomerRepository
from src.use_cases.errors.use_case_error import UseCaseError

@dataclass
class CreateCustomerInput:
    name: str
    email: str

class CreateCustomer:
    def __init__(self, id_gen: IdGenerator, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo
        self.id_gen = id_gen

    def execute(self, input: CreateCustomerInput) -> str:
        '''
        Creates a new Customer if not exists
        :param input: CreateCustomerInput
        return ID: str
        '''
        if(self.customer_repo.email_exists(input.email)):
            raise UseCaseError("Customer already exists")
        ID = self.id_gen.generate()
        customer = Customer(id=ID, name=input.name, email=input.email)
        self.customer_repo.save(customer=customer)
        return ID