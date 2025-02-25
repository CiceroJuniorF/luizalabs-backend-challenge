
from dataclasses import dataclass

from src.application.errors.application_error import ApplicationError
from src.application.errors.application_errors_enum import ApplicationErrors
from src.domain.interfaces.repositories.customer_repository import CustomerRepository
from src.domain.interfaces.repositories.favorite_product_repository import FavoriteProductRepository


@dataclass
class RemoveCustomerInput:
    customer_id: str
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
    
    @classmethod
    def from_dict(cls, input_value):
        return cls(**input_value)
        

class RemoveCustomer:
    def __init__(self, customer_repository: CustomerRepository, favorite_product_repository: FavoriteProductRepository):
        self.customer_repository = customer_repository
        self.favorite_product_repository = favorite_product_repository

    async def execute(self, remove_customer_input: RemoveCustomerInput):
        """
        Executes the removal of a customer and their associated favorite products.
        Args:
            remove_customer_input (RemoveCustomerInput): The input to remove a customer.
        Raises:
            ApplicationError: If the customer is not found.
        """
       
        customer = await self.customer_repository.find_by_id(remove_customer_input.customer_id)
        if not customer:
            raise ApplicationError(ApplicationErrors.NOT_FOUND, 'Customer not found')
        await self.favorite_product_repository.remove_by_customer_id(remove_customer_input.customer_id)
        await self.customer_repository.remove(customer.id)