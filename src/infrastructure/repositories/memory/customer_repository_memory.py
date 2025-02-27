from typing import List, Optional
from src.domain.entities.customer import Customer
from src.domain.interfaces.repositories.customer_repository import CustomerRepository
from src.infrastructure.repositories.errors import NotExists


class CustomerRepositoryMemory(CustomerRepository):
    def __init__(self):
        self.customers = []

    async def save(self, customer: Customer):
        self.customers.append(customer)
        return customer.id

    async def find_by_id(self, customer_id: str) -> Optional[Customer]:
        for customer in self.customers:
            if customer.id == customer_id:
                return customer
        return None

    async def email_exists(self, email: str) -> bool:
        return any(filter(lambda c: c.email == email, self.customers))
    
    async def remove(self, id: str) -> bool:
        for customer in self.customers:
            if customer.id == id:
                self.customers.remove(customer)
                print(self.customers)
                return True
        return False