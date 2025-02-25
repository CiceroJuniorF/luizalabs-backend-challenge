
from src.application.errors.application_error import ApplicationError
from src.application.errors.application_errors_enum import ApplicationErrors
from src.domain.entities.favorite_product import FavoriteProduct
from src.domain.interfaces.gateway.product_service import ProductService
from src.domain.interfaces.id_generator import IdGenerator
from src.domain.interfaces.repositories.customer_repository import CustomerRepository
from src.domain.interfaces.repositories.favorite_product_repository import FavoriteProductRepository


class AddProductToFavoritesInput:

    customer_id: str
    product_id: str
    def __init__(self, customer_id:str, product_id:str):
        self.customer_id = customer_id
        self.product_id = product_id    
    @classmethod
    def from_dict(cls, input_value):
        return cls(**input_value)

class AddProductToFavorites:
    def __init__(self, 
                 customer_repository:CustomerRepository, 
                 favorite_product_repository: FavoriteProductRepository, 
                 id_gen: IdGenerator, product_service: ProductService):
        self.product_service = product_service
        self.customer_repository = customer_repository
        self.favorite_product_repository = favorite_product_repository
        self.id_gen = id_gen

    def execute(self, input: AddProductToFavoritesInput):
        customer = self.customer_repository.find_by_id(input.customer_id)
        if not customer:
            raise ApplicationError(ApplicationErrors.NOT_FOUND, 'Customer not found')
        
        product = self.product_service.get(input.product_id)
        if not product:
            raise ApplicationError(ApplicationErrors.NOT_FOUND, 'Product not found')
        
        if(self.favorite_product_repository.exists_product_in_customer_favorites(input.customer_id, input.product_id)):
            raise ApplicationError(ApplicationErrors.CONFLICT, "Product already exists in favorites")
            
        favorite_product = FavoriteProduct(
            id=self.id_gen.generate(),
            customer_id=input.customer_id,
            product_id=input.product_id,
            title=product.title,
            image=product.image,
            price=product.price
        )
        return self.favorite_product_repository.add(favorite_product)