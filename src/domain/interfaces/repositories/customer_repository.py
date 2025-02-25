from abc import ABC, abstractmethod

from src.domain.entities.customer import Customer

class CustomerRepository(ABC):
    
    @abstractmethod
    def save(self, Customer:Customer) -> str: # pragma: no cover 
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Customer: # pragma: no cover 
        pass

    @abstractmethod
    def email_exists(self, email: str) -> bool: # pragma: no cover 
        pass