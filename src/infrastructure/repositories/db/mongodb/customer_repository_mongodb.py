from motor.motor_asyncio import AsyncIOMotorClient
from src.domain.entities.customer import Customer
from src.domain.interfaces.repositories.customer_repository import CustomerRepository

class CustomerRepositoryMongoDB(CustomerRepository):
    def __init__(self, uri: str, database_name: str, collection_name: str, mongo_username: str, mongo_password: str):
        self.client = AsyncIOMotorClient(uri, username=mongo_username, password=mongo_password)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    async def save(self, customer: Customer):
        customer_dict = customer.to_dict()
        customer_dict["_id"] = customer.id
        del customer_dict["id"]
        if await self.collection.find_one({"_id": customer.id}):
            result = await self.collection.replace_one({"_id": customer.id}, customer_dict)
            return str(result.upserted_id)
        else:
            result = await self.collection.insert_one(customer_dict)
            return str(result.inserted_id) 

    async def find_by_id(self, customer_id: str) -> Customer:
        customer_data = await self.collection.find_one({"_id": customer_id})
        if customer_data:
            customer_data["id"] = customer_data["_id"]
            del customer_data["_id"]
            return Customer.from_dict(customer_data)
        return None

    async def email_exists(self, email: str) -> bool:
        customer_data = await self.collection.find_one({"email": email})
        return customer_data is not None

    async def remove(self, customer_id: str) -> bool:
        result = await self.collection.delete_one({"_id": customer_id})
        return result.deleted_count > 0