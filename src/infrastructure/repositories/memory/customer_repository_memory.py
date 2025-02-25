from typing import List
from src.domain.entities.customer import Customer
from src.domain.interfaces.repositories.customer_repository import CustomerRepository
from src.infrastructure.repositories.errors import NotExists


class CustomerRepositoryMemory(CustomerRepository):
    def __init__(self):
        self.customers = []

    def save(self, customer: Customer):
        self.customers.append(customer)
        return customer.id

    def find_by_id(self, customer_id: str) -> Customer:
        for customer in self.customers:
            if customer.id == customer_id:
                return customer

        return None

    def email_exists(self, email: str) -> bool:
        return any(filter(lambda c: c.email == email, self.customers))