from src.domain.entities.customer import Customer
from src.infrastructure.queries.customer_list_query import CustomerListQuery, CustomerListQueryOutput
from motor.motor_asyncio import AsyncIOMotorClient

class CustomerListQueryMongoDB(CustomerListQuery):
    def __init__(self, uri: str, database_name: str, collection_name: str, mongo_username: str, mongo_password: str):
        self.client = AsyncIOMotorClient(uri, username=mongo_username, password=mongo_password)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    async def list(self, page: int = 1, size: int = 10) -> CustomerListQueryOutput:
        total = await self.collection.count_documents({})
        total_pages = (total + size - 1) // size
        cursor = self.collection.find().skip((page - 1) * size).limit(size)
        items = await cursor.to_list(length=size)
        items = [Customer.from_dict({
            "id": str(item.get("_id")),
            "name": item.get("name"),
            "email": item.get("email")
        }) for item in items]
        return CustomerListQueryOutput(page, size, total_pages, total, items)