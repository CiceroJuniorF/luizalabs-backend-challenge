from typing import List
from src.domain.entities.customer import Customer
from src.infrastructure.queries.customer_list_query import CustomerListQuery, CustomerListQueryOutput
from src.infrastructure.repositories.memory.customer_repository_memory import CustomerRepositoryMemory


class CustomerListMemoryQuery(CustomerListQuery):
    def __init__(self, customer_repository: CustomerRepositoryMemory):
        self.customer_repository = customer_repository

    async def list(self, page:int = 1, size:int=10) -> CustomerListQueryOutput:
        total = len(self.customer_repository.customers)
        total_pages = (total + size - 1) // size
        start = (page - 1) * size
        end = start + size
        items = self.customer_repository.customers[start:end]
        return CustomerListQueryOutput(page, size, total_pages, total, items)