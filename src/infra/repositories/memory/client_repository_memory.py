from typing import List
from src.domain.entities.client import Client
from src.domain.interfaces.repositories.client_repository import ClientRepository
from src.infra.repositories.errors import NotExists


class ClientRepositoryMemory(ClientRepository):
    def __init__(self):
        self.clients = []

    def save(self, client: Client):
        self.clients.append(client)

    def find_by_id(self, client_id: str) -> Client:
        for client in self.clients:
            if client.id == client_id:
                return client

        raise NotExists('Client', client_id)

    def exists(self, name: str, email: str) -> bool:
        return any(filter(lambda x: x.name == name and x.email == email, self.clients))