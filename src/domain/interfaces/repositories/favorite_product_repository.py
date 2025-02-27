
from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.favorite_product import FavoriteProduct



class FavoriteProductRepository(ABC):
    @abstractmethod
    async def add(self, favorite_product: FavoriteProduct) -> str: # pragma: no cover 
        pass

    @abstractmethod
    async def exists_product_in_customer_favorites(self, customer_id: str, product_id: str) -> bool: # pragma: no cover
        pass

    @abstractmethod
    async def remove(self, customer_id:str, product_id: str) -> bool: # pragma: no cover 
        pass

    @abstractmethod
    async def remove_by_customer_id(self, customer_id: str) -> bool:# pragma: no cover 
        pass
