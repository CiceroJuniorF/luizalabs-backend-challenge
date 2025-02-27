from fastapi import APIRouter, Depends

from src.application.add_product_to_favorites import AddProductToFavorites, AddProductToFavoritesInput
from src.application.remove_product_from_favorites import RemoveProductFromFavorites, RemoveProductFromFavoritesInput
from src.dependencies import add_favorite_product_use_case, remove_favorite_product_use_case
from src.presentation.command.favorite_product_messages import AddProductToFavoritesResponse


router = APIRouter(prefix="/customer/{customer_id}/favorite/product", tags=["Customer", "Favorites"])

# ADD FAVORITE PRODUCT
@router.post("/add/{product_id}", 
             status_code=201, 
             summary="Add a product to customer's favorites",
             response_model=AddProductToFavoritesResponse,
             responses={
                    201: {"description": "Product added successfully"},
                    400: {"description": "Invalid data", "content": {"application/json": {"example": {"message": "Invalid data"}}}},
                    404: {"description": "Conflict (Customer or Product not exists)", "content": {"application/json": {"example": {"message": "Customer not exists"}}}}
            })
async def add_favorite_product(customer_id: str, 
                                product_id: str, 
                                add_favorite_product: AddProductToFavorites = Depends(add_favorite_product_use_case)) -> None:
    id = await add_favorite_product.execute(AddProductToFavoritesInput.from_dict({"customer_id": customer_id, "product_id": product_id}))
    return AddProductToFavoritesResponse.create(id=id)

# REMOVE FAVORITE PRODUCT
@router.delete("/remove/{product_id}", 
                status_code=204, 
                summary="Remove a product from customer's favorites",
                responses={
                    204: {"description": "Product removed successfully"},
                    404: {"description": "Conflict (Customer or Product not exists in favorites)", "content": {"application/json": {"example": {"message": "Customer not exists"}}}}
            })
async def remove_favorite_product(customer_id: str, 
                                product_id: str, 
                                remove_favorite_product: RemoveProductFromFavorites = Depends(remove_favorite_product_use_case)) -> None:
    await remove_favorite_product.execute(RemoveProductFromFavoritesInput.from_dict({"customer_id": customer_id, "product_id": product_id}))