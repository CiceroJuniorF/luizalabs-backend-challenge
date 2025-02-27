from typing import List
from src.domain.entities.favorite_product import FavoriteProduct
from src.infrastructure.queries.favorite_product_list_query import FavoriteProductListQuery, FavoriteProductListQueryOutput
from src.infrastructure.repositories.memory.favorite_product_repository_memory import FavoriteProductRepositoryMemory


class FavoriteProductListMemoryQuery(FavoriteProductListQuery):
    def __init__(self, favorite_repository: FavoriteProductRepositoryMemory):
        self.favorite_repository = favorite_repository

    async def list(self, customer_id: str, page:int = 1, size:int=10) -> FavoriteProductListQueryOutput:
        favorites = [ favorite for favorite in self.favorite_repository.favorite_products if favorite.customer_id == customer_id ]
        total = len(favorites)
        total_pages = (total + size - 1) // size
        start = (page - 1) * size
        end = start + size
        items = favorites[start:end]
        return FavoriteProductListQueryOutput(page, size, total_pages, total, items)