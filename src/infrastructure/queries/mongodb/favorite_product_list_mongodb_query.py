from src.domain.entities.favorite_product import FavoriteProduct
from src.infrastructure.queries.favorite_product_list_query import FavoriteProductListQuery, FavoriteProductListQueryOutput
from motor.motor_asyncio import AsyncIOMotorClient

class FavoriteProductListQueryMongoDB(FavoriteProductListQuery):
    def __init__(self, uri: str, database_name: str, collection_name: str, mongo_username: str, mongo_password: str):
        self.client = AsyncIOMotorClient(uri, username=mongo_username, password=mongo_password)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    async def list(self, customer_id: str,  page: int = 1, size: int = 10) -> FavoriteProductListQueryOutput:
        query = {"customer_id": customer_id}
        total = await self.collection.count_documents(query)
        total_pages = (total + size - 1) // size
        cursor = self.collection.find(query).skip((page - 1) * size).limit(size)
        items = await cursor.to_list(length=size)
        items = [FavoriteProduct.from_dict({
            "id": str(item.get("_id")),
            "customer_id": str(item.get("customer_id")),
            "product_id": item.get("product_id"),
            "title": item.get("title"),
            "price": item.get("price"),
            "image": item.get("image")
        }) for item in items]
        return FavoriteProductListQueryOutput(page, size, total_pages, total, items)