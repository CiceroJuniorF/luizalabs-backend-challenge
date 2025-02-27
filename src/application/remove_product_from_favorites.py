
from src.application.errors.application_error import ApplicationError
from src.application.errors.application_errors_enum import ApplicationErrors
from src.domain.interfaces.repositories.customer_repository import CustomerRepository
from src.domain.interfaces.repositories.favorite_product_repository import \
    FavoriteProductRepository


class RemoveProductFromFavoritesInput:

    customer_id: str
    product_id: str
    def __init__(self, customer_id:str, product_id:str):
        self.customer_id = customer_id
        self.product_id = product_id
    @classmethod
    def from_dict(cls, input_value):
        return cls(**input_value)

class RemoveProductFromFavorites:
    def __init__(self,
                 customer_repository:CustomerRepository,
                 favorite_product_repository: FavoriteProductRepository):
        self.favorite_product_repository = favorite_product_repository
        self.customer_repository = customer_repository

    async def execute(self, input: RemoveProductFromFavoritesInput):
        """
        Removes a product from the favorites list.
        Args:
            input (RemoveProductFromFavoritesInput): The input containing the ID of the product to be removed.
        Returns:
            bool: True if the product was successfully removed, False otherwise.
        """
        customer = await self.customer_repository.find_by_id(input.customer_id)
        if(not customer):
            raise ApplicationError(ApplicationErrors.NOT_FOUND, 'Customer not found')
        product_in_customer_favorites = await self.favorite_product_repository.exists_product_in_customer_favorites(customer_id=input.customer_id, product_id=input.product_id) 
        if(not product_in_customer_favorites):
            raise ApplicationError(ApplicationErrors.NOT_FOUND, 'Product not found')
        return await self.favorite_product_repository.remove(customer_id=input.customer_id, product_id=input.product_id)