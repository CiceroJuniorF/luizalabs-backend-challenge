from abc import ABC, abstractmethod

from src.domain.entities.client import Client

class ClientRepository(ABC):
    
    @abstractmethod
    def save(self, client:Client) -> None: # pragma: no cover 
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Client: # pragma: no cover 
        pass

    @abstractmethod
    def exists(self, name: str, email: str) -> bool: # pragma: no cover 
        pass