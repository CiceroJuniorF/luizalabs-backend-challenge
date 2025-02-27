
from dataclasses import dataclass
from typing import List

from src.domain.entities.favorite_product import FavoriteProduct


@dataclass
class AddProductToFavoritesResponse():
    id: str
    def __init__(self, id):
        self.id = id
    
    @classmethod
    def create(self, id: str):
        return AddProductToFavoritesResponse(id=id)
@dataclass
class FavoriteProductListResponse():
    page: int
    size: int
    total_pages: int
    total: int
    items: List[FavoriteProduct]

    @classmethod
    def create(self, items: List[FavoriteProduct], page: int, size: int, total_pages: int, total: int):
        return FavoriteProductListResponse(items=items, page=page, size=size, total_pages=total_pages, total=total)