from unittest.mock import AsyncMock, patch
from src.application.errors.application_error import ApplicationError
from src.application.errors.application_errors_enum import ApplicationErrors
from src.application.remove_customer import RemoveCustomer, RemoveCustomerInput
from src.domain.entities.customer import Customer
from src.domain.interfaces.repositories.customer_repository import \
    CustomerRepository
from src.domain.interfaces.repositories.favorite_product_repository import \
    FavoriteProductRepository

CUSTOMER_ID='eefc9802-1d7d-4aec-8190-8838ed66fbba'
customer = {
        'id': CUSTOMER_ID,
        'name': 'customer_name',
        'email': 'customer_email@mail.com'
    }
def __config_default_mocks(mock_customer_repository: CustomerRepository, mock_favorite_product_repository: FavoriteProductRepository):
    # Mocking services
    mock_customer_repository.find_by_id = AsyncMock()
    mock_customer_repository.find_by_id.return_value = Customer.from_dict(customer)
    mock_customer_repository.remove = AsyncMock()
    mock_customer_repository.remove.return_value = True
    mock_favorite_product_repository.remove_by_customer_id = AsyncMock()
    mock_favorite_product_repository.remove_by_customer_id.return_value = True



@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
@patch('src.domain.interfaces.repositories.favorite_product_repository.FavoriteProductRepository')
async def test_should_remove_customer_and_favorite_list(mock_customer_repository: CustomerRepository, 
                                  mock_favorite_product_repository: FavoriteProductRepository
                                ):
    # Mocking services
    __config_default_mocks(mock_customer_repository, mock_favorite_product_repository)

    await RemoveCustomer(mock_customer_repository, mock_favorite_product_repository)\
        .execute(RemoveCustomerInput.from_dict({
            'customer_id': CUSTOMER_ID
        }))

    mock_customer_repository.find_by_id.assert_called_once()
    mock_customer_repository.find_by_id.assert_called_with(CUSTOMER_ID)
    mock_favorite_product_repository.remove_by_customer_id.assert_called_once()
    mock_favorite_product_repository.remove_by_customer_id.assert_called_with(CUSTOMER_ID)

@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
@patch('src.domain.interfaces.repositories.favorite_product_repository.FavoriteProductRepository')
async def test_shouldnt_remove_customer_because_not_exists(mock_customer_repository: CustomerRepository, 
                                  mock_favorite_product_repository: FavoriteProductRepository
                                ):
    # Mocking services
    __config_default_mocks(mock_customer_repository, mock_favorite_product_repository)
    # !Override default mock_customer_repository.find_by_id to return None
    mock_customer_repository.find_by_id.return_value = None
    try:
        await RemoveCustomer(mock_customer_repository, mock_favorite_product_repository)\
            .execute(RemoveCustomerInput.from_dict({
                'customer_id': CUSTOMER_ID
            }))
    except ApplicationError as e:
        assert e.error == ApplicationErrors.NOT_FOUND
        assert str(e) == 'Customer not found'
        mock_customer_repository.find_by_id.assert_called_once()
        mock_customer_repository.find_by_id.assert_called_with(CUSTOMER_ID)