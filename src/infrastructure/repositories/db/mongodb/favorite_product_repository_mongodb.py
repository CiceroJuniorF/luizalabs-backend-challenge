from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from src.domain.entities.favorite_product import FavoriteProduct
from src.domain.interfaces.repositories.favorite_product_repository import FavoriteProductRepository

class FavoriteProductRepositoryMongoDB(FavoriteProductRepository):
    
    def __init__(self, uri: str, database_name: str, collection_name: str, mongo_username: str, mongo_password: str):
        self.client = AsyncIOMotorClient(uri, username=mongo_username, password=mongo_password)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    async def add(self, favorite_product: FavoriteProduct) -> str:
        result = await self.collection.insert_one(favorite_product.to_dict())
        return str(result.inserted_id)

    async def exists_product_in_customer_favorites(self, customer_id: str, product_id: str) -> bool:
        favorite_product = await self.collection.find_one({
            'customer_id': ObjectId(customer_id),
            'product_id': product_id
        })
        return favorite_product is not None

    async def remove(self, customer_id: str, product_id: str) -> bool:
        result = await self.collection.delete_one({
            'customer_id': ObjectId(customer_id),
            'product_id': product_id
        })
        return result.deleted_count > 0

    async def remove_by_customer_id(self, customer_id: str) -> bool:
        result = await self.collection.delete_many({
            'customer_id': ObjectId(customer_id)
        })
        return result.deleted_count > 0