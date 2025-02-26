from unittest.mock import AsyncMock, patch
from src.application.remove_product_from_favorites import RemoveProductFromFavorites, RemoveProductFromFavoritesInput
from src.application.errors.application_error import ApplicationError
from src.application.errors.application_errors_enum import ApplicationErrors
from src.domain.interfaces.repositories.favorite_product_repository import FavoriteProductRepository

FAVORITE_PRODUCT_ID = '246a7903-056a-4a40-b3d1-ad406a891b83'

@patch('src.domain.interfaces.repositories.favorite_product_repository.FavoriteProductRepository')
async def test_should_remove_product_from_favorites(mock_favorite_product_repository: FavoriteProductRepository):
    mock_favorite_product_repository.find_by_id = AsyncMock()
    mock_favorite_product_repository.remove = AsyncMock()
    mock_favorite_product_repository.find_by_id.return_value = True
    mock_favorite_product_repository.remove.return_value = True
    remove_product_from_favorites = RemoveProductFromFavorites(mock_favorite_product_repository)
    input_data = RemoveProductFromFavoritesInput(id=FAVORITE_PRODUCT_ID)
    
    result = await remove_product_from_favorites.execute(input_data)

    assert result is True
    mock_favorite_product_repository.find_by_id.assert_awaited_once_with(FAVORITE_PRODUCT_ID)
    mock_favorite_product_repository.remove.assert_awaited_once_with(FAVORITE_PRODUCT_ID)

@patch('src.domain.interfaces.repositories.favorite_product_repository.FavoriteProductRepository')
async def test_shouldnt_remove_product_from_favorites_because_not_found(mock_favorite_product_repository: FavoriteProductRepository):
    mock_favorite_product_repository.find_by_id = AsyncMock()
    mock_favorite_product_repository.remove = AsyncMock()
    mock_favorite_product_repository.find_by_id.return_value = False
    mock_favorite_product_repository.remove.return_value = False
    remove_product_from_favorites = RemoveProductFromFavorites(mock_favorite_product_repository)
    input_data = RemoveProductFromFavoritesInput(id=FAVORITE_PRODUCT_ID)
    try:
        await remove_product_from_favorites.execute(input_data)
    except ApplicationError as e:
        assert e.error == ApplicationErrors.NOT_FOUND
        assert str(e) == 'Product not found'
        mock_favorite_product_repository.find_by_id.assert_awaited_once_with(FAVORITE_PRODUCT_ID)
        mock_favorite_product_repository.remove.assert_not_awaited()
    

  