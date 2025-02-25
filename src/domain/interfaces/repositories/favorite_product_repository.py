
from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.favorite_product import FavoriteProduct



class FavoriteProductRepository(ABC):
    @abstractmethod
    def add(self, favorite_product: FavoriteProduct) -> str: # pragma: no cover 
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> FavoriteProduct: # pragma: no cover 
        pass

    @abstractmethod
    def exists_product_in_customer_favorites(self, customer_id: str, product_id: str) -> bool: # pragma: no cover
        pass

    @abstractmethod
    def remove(self, id: str) -> bool: # pragma: no cover 
        pass

    @abstractmethod
    def remove_by_customer_id(self, customer_id: str) -> bool:# pragma: no cover 
        pass

    @abstractmethod
    def remove_by_customer_id_and_product_id(self, customer_id: str, product_id: str) -> bool:# pragma: no cover 
        pass