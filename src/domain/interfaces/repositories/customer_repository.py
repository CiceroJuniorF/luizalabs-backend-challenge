from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.customer import Customer

class CustomerRepository(ABC):
    
    @abstractmethod
    async def save(self, customer:Customer) -> str: # pragma: no cover 
        pass

    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[Customer]: # pragma: no cover 
        pass

    @abstractmethod
    async def email_exists(self, email: str) -> bool: # pragma: no cover 
        pass