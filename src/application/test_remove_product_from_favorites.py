from unittest.mock import AsyncMock, patch
from src.application.remove_product_from_favorites import RemoveProductFromFavorites, RemoveProductFromFavoritesInput
from src.application.errors.application_error import ApplicationError
from src.application.errors.application_errors_enum import ApplicationErrors
from src.domain.interfaces.repositories.customer_repository import CustomerRepository
from src.domain.interfaces.repositories.favorite_product_repository import FavoriteProductRepository

PRODUCT_ID = '246a7903-056a-4a40-b3d1-ad406a891b83'
CUSTOMER_ID='eefc9802-1d7d-4aec-8190-8838ed66fbba'
customer = {
        'id': CUSTOMER_ID,
        'name': 'customer_name',
        'email': 'customer_email@mail.com'
    }

def __config_default_mocks(mock_favorite_product_repository, mock_customer_repository):
    # Mocking services
    mock_favorite_product_repository.exists_product_in_customer_favorites = AsyncMock()
    mock_favorite_product_repository.remove = AsyncMock()
    mock_favorite_product_repository.exists_product_in_customer_favorites.return_value = True
    mock_favorite_product_repository.remove.return_value = True
    mock_customer_repository.find_by_id = AsyncMock()
    mock_customer_repository.find_by_id.return_value = customer

@patch('src.domain.interfaces.repositories.favorite_product_repository.FavoriteProductRepository')
@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
async def test_should_remove_product_from_favorites(mock_favorite_product_repository: FavoriteProductRepository, mock_customer_repository: CustomerRepository):

    __config_default_mocks(mock_favorite_product_repository, mock_customer_repository)
    remove_product_from_favorites = RemoveProductFromFavorites(mock_customer_repository, mock_favorite_product_repository)
    input_data = RemoveProductFromFavoritesInput.from_dict({"customer_id": CUSTOMER_ID, "product_id": PRODUCT_ID})
    result = await remove_product_from_favorites.execute(input_data)

    assert result is True
    mock_customer_repository.find_by_id.assert_awaited_once_with(CUSTOMER_ID)
    mock_favorite_product_repository.exists_product_in_customer_favorites.assert_awaited_once_with(customer_id=CUSTOMER_ID, product_id=PRODUCT_ID)
    mock_favorite_product_repository.remove.assert_awaited_once_with(customer_id=CUSTOMER_ID, product_id=PRODUCT_ID)

@patch('src.domain.interfaces.repositories.favorite_product_repository.FavoriteProductRepository')
@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
async def test_shouldnt_remove_product_from_favorites_because_customer_not_found(mock_favorite_product_repository: FavoriteProductRepository, mock_customer_repository: CustomerRepository):
    __config_default_mocks(mock_favorite_product_repository, mock_customer_repository)
    remove_product_from_favorites = RemoveProductFromFavorites(mock_customer_repository, mock_favorite_product_repository)
    input_data = RemoveProductFromFavoritesInput.from_dict({"customer_id": CUSTOMER_ID, "product_id": PRODUCT_ID})
    # !Override default mock_customer_repository. to return False
    mock_customer_repository.find_by_id.return_value = None
    try:
        await remove_product_from_favorites.execute(input_data)
    except ApplicationError as e:
        assert e.error == ApplicationErrors.NOT_FOUND
        assert str(e) == 'Customer not found'
        mock_customer_repository.find_by_id.assert_awaited_once_with(CUSTOMER_ID)
        mock_favorite_product_repository.remove.assert_not_awaited()

@patch('src.domain.interfaces.repositories.favorite_product_repository.FavoriteProductRepository')
@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
async def test_shouldnt_remove_product_from_favorites_because_product_not_found(mock_favorite_product_repository: FavoriteProductRepository, mock_customer_repository: CustomerRepository):
    __config_default_mocks(mock_favorite_product_repository, mock_customer_repository)
    remove_product_from_favorites = RemoveProductFromFavorites(mock_customer_repository, mock_favorite_product_repository)
    input_data = RemoveProductFromFavoritesInput.from_dict({"customer_id": CUSTOMER_ID, "product_id": PRODUCT_ID})
    # !Override default mock_customer_repository. to return False
    mock_favorite_product_repository.exists_product_in_customer_favorites.return_value = False
    try:
        await remove_product_from_favorites.execute(input_data)
    except ApplicationError as e:
        assert e.error == ApplicationErrors.NOT_FOUND
        assert str(e) == 'Product not found'
        mock_customer_repository.find_by_id.assert_awaited_once_with(CUSTOMER_ID)
        mock_favorite_product_repository.exists_product_in_customer_favorites.assert_awaited_once_with(customer_id=CUSTOMER_ID, product_id=PRODUCT_ID)
        mock_favorite_product_repository.remove.assert_not_awaited()
    

  