
from dataclasses import dataclass

from src.application.errors.application_error import ApplicationError
from src.application.errors.application_errors_enum import ApplicationErrors
from src.domain.interfaces.repositories.customer_repository import CustomerRepository


@dataclass
class UpdateCustomerInput:
    id: str
    name: str
    email: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class UpdateCustomer:
    def __init__(self, customer_repository:CustomerRepository):
        self.customer_repository = customer_repository
    
    async def execute(self, input: UpdateCustomerInput) -> str:
        """
        Updates the customer information.
        Args:
            input (UpdateCustomerInput): The input data containing the customer updated information.
        Returns:
            str: The ID of the updated customer.
        Raises:
            ApplicationError: If the customer is not found.
        """
        customer = await self.customer_repository.find_by_id(input.id)
        if not customer:
            raise ApplicationError(ApplicationErrors.NOT_FOUND, 'Customer not found')
        customer.name = input.name
        customer.email = input.email
        if(customer.is_valid_to_save()):
            await self.customer_repository.save(customer)

        return customer.id