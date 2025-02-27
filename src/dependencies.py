from fastapi import Depends
from fastapi.security import OAuth2, OAuth2PasswordBearer
from src.application.add_product_to_favorites import AddProductToFavorites
from src.application.create_customer import CreateCustomer
from src.application.remove_customer import RemoveCustomer
from src.application.remove_product_from_favorites import RemoveProductFromFavorites
from src.application.update_customer import UpdateCustomer
from src.config import MONGODB_DB, MONGODB_PASSWORD, MONGODB_URL, MONGODB_USERNAME, USE_IN_MEMORY
from src.domain.entities.favorite_product import FavoriteProduct
from src.domain.interfaces.gateway.product_service import ProductService
from src.domain.interfaces.repositories.customer_repository import CustomerRepository
from src.domain.interfaces.repositories.favorite_product_repository import FavoriteProductRepository
from src.infrastructure.gateway.product_service_memory import ProductServiceMemory
from src.infrastructure.mongodb_id_generator import MongoDBIdGenerator
from src.infrastructure.repositories.db.mongodb.customer_repository_mongodb import CustomerRepositoryMongoDB
from src.infrastructure.repositories.db.mongodb.favorite_product_repository_mongodb import FavoriteProductRepositoryMongoDB
from src.infrastructure.repositories.memory.customer_repository_memory import CustomerRepositoryMemory
from src.infrastructure.repositories.memory.favorite_product_repository_memory import FavoriteProductRepositoryMemory
from src.infrastructure.security.oauth2_client_credentials_service import OAuth2ClientCredentialsService
from src.infrastructure.uuid_id_generator import UUIDIdGenerator
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowClientCredentials


# REPOSITORIES
if USE_IN_MEMORY:
    id_gen = UUIDIdGenerator()
    customer_repository: CustomerRepository = CustomerRepositoryMemory()
    favorite_repository: FavoriteProductRepository = FavoriteProductRepositoryMemory()
else:
    id_gen = MongoDBIdGenerator()
    customer_repository: CustomerRepository = CustomerRepositoryMongoDB(
        collection_name="customers", 
        database_name=MONGODB_DB,
        mongo_password=MONGODB_PASSWORD,
        mongo_username=MONGODB_USERNAME,
        uri=MONGODB_URL)

    favorite_repository: FavoriteProductRepository = FavoriteProductRepositoryMongoDB(
        collection_name="favorite_products", 
        database_name=MONGODB_DB,
        mongo_password=MONGODB_PASSWORD,
        mongo_username=MONGODB_USERNAME,
        uri=MONGODB_URL)

# Está mockado, mas poderia ser um serviço real
product_service: ProductService = ProductServiceMemory()

# CUSTOMER
def create_customer_use_case() -> CreateCustomer:
    return CreateCustomer(id_gen, customer_repository)

def remove_customer_use_case() -> RemoveCustomer:
    return RemoveCustomer(customer_repository, favorite_repository)

def update_customer_use_case() -> UpdateCustomer:
    return UpdateCustomer(customer_repository)

# FAVORITE PRODUCT
def add_favorite_product_use_case() -> FavoriteProduct:
    return AddProductToFavorites(customer_repository, favorite_repository, id_gen, product_service)

def remove_favorite_product_use_case() -> FavoriteProduct:
    return RemoveProductFromFavorites(customer_repository, favorite_repository)

def oauth2_client_credentials_service() -> OAuth2ClientCredentialsService:
    return OAuth2ClientCredentialsService()

oauth2_scheme = OAuth2(
    flows=OAuthFlowsModel(
        clientCredentials=OAuthFlowClientCredentials(
            tokenUrl="api/auth/token",
        ),
        
        
    )
)

def authorize(token: str = Depends(oauth2_scheme)):
    token = token.replace("Bearer ", "") # Remove Bearer from token
    return OAuth2ClientCredentialsService().authorize(token)


   
