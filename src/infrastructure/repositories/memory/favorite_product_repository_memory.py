from typing import List, Optional
from src.domain.entities.favorite_product import FavoriteProduct
from src.domain.interfaces.repositories.favorite_product_repository import FavoriteProductRepository


class FavoriteProductRepositoryMemory(FavoriteProductRepository):
    
    def __init__(self):
        self.favorite_products:List[FavoriteProduct] = []

 
    async def add(self, favorite_product: FavoriteProduct) -> str:
        self.favorite_products.append(favorite_product)
        return favorite_product.id


    async def exists_product_in_customer_favorites(self, customer_id: str, product_id: str) -> bool: 
        return any(filter(lambda favorite_product: favorite_product.customer_id == customer_id and favorite_product.product_id == product_id, self.favorite_products))

    async def remove(self, customer_id: str, product_id) -> bool: 
        favorite_products = list(filter(lambda favorite_product: favorite_product.customer_id == customer_id 
                                        and favorite_product.product_id == product_id, self.favorite_products))
        if favorite_products:
            self.favorite_products.remove(favorite_products[0])
            return True
        return False

    async def remove_by_customer_id(self, customer_id: str) -> bool:
        favorite_products = list(filter(lambda favorite_product: favorite_product.customer_id == customer_id, self.favorite_products))
        if favorite_products:
            self.favorite_products.remove(favorite_products[0])
            return True
        return False

