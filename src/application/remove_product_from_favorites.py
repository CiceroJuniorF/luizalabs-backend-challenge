
from src.application.errors.application_error import ApplicationError
from src.application.errors.application_errors_enum import ApplicationErrors
from src.domain.interfaces.repositories.favorite_product_repository import \
    FavoriteProductRepository


class RemoveProductFromFavoritesInput:

    id: str
    def __init__(self, id:str):
        self.id = id
    @classmethod
    def from_dict(cls, input_value):
        return cls(**input_value)

class RemoveProductFromFavorites:
    def __init__(self,
                 favorite_product_repository: FavoriteProductRepository):
        self.favorite_product_repository = favorite_product_repository

    async def execute(self, input: RemoveProductFromFavoritesInput):
        """
        Removes a product from the favorites list.
        Args:
            input (RemoveProductFromFavoritesInput): The input containing the ID of the product to be removed.
        Returns:
            bool: True if the product was successfully removed, False otherwise.
        """
        product = await self.favorite_product_repository.find_by_id(input.id) 
        if(not product):
            raise ApplicationError(ApplicationErrors.NOT_FOUND, 'Product not found')
        return await self.favorite_product_repository.remove(input.id)