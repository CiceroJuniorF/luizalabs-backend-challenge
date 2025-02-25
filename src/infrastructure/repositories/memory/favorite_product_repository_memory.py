from typing import List
from src.domain.entities.favorite_product import FavoriteProduct
from src.domain.interfaces.repositories.favorite_product_repository import FavoriteProductRepository


class FavoriteProductRepositoryMemory(FavoriteProductRepository):
    
    def __init__(self):
        self.favorite_products:List[FavoriteProduct] = []

 
    def add(self, favorite_product: FavoriteProduct) -> str:
        self.favorite_products.append(favorite_product)
        return favorite_product.id

   
    def find_by_id(self, id: str) -> FavoriteProduct: 
        favorite_products = list(filter(lambda favorite_product: favorite_product.id == id, self.favorite_products))
        return favorite_products[0] if favorite_products else None

    def exists_product_in_customer_favorites(self, customer_id: str, product_id: str) -> bool: 
        return any(filter(lambda favorite_product: favorite_product.customer_id == customer_id and favorite_product.product_id == product_id, self.favorite_products))

    def remove(self, id: str) -> bool: 
        pass

    def remove_by_customer_id(self, customer_id: str) -> bool:
        pass

    def remove_by_customer_id_and_product_id(self, customer_id: str, product_id: str) -> bool:
        pass