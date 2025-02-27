
from dataclasses import dataclass


@dataclass
class AddProductToFavoritesResponse():
    id: str
    def __init__(self, id):
        self.id = id
    
    @classmethod
    def create(self, id: str):
        return AddProductToFavoritesResponse(id=id)