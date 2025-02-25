import unittest
from unittest.mock import patch

from src.application.add_product_to_favorites import AddProductToFavorites, AddProductToFavoritesInput
from src.application.errors.application_error import ApplicationError
from src.application.errors.application_errors_enum import ApplicationErrors
from src.domain.entities.customer import Customer

from src.domain.interfaces.gateway.product_service import ProductOutput, ProductService
from src.domain.interfaces.id_generator import IdGenerator
from src.domain.interfaces.repositories.customer_repository import CustomerRepository
from src.domain.interfaces.repositories.favorite_product_repository import FavoriteProductRepository


CUSTOMER_ID='eefc9802-1d7d-4aec-8190-8838ed66fbba'
PRODUCT_ID='20d4e197-a909-4c37-a92b-2bb0ddcd814f'
FAVORITE_PRODUCT_ID = '246a7903-056a-4a40-b3d1-ad406a891b83'

def __config_default_mocks(mock_customer_repository, mock_favorite_product_repository, mock_id_generator, mock_product_service):
    # Mocking services
    mock_customer_repository.find_by_id.return_value = Customer.from_dict({
        'id': CUSTOMER_ID,
        'name': 'customer_name',
        'email': 'customer_email@mail.com'
    })
    mock_favorite_product_repository.exists_product_in_customer_favorites.return_value = False
    mock_id_generator.generate.return_value = FAVORITE_PRODUCT_ID
    mock_favorite_product_repository.add.return_value = FAVORITE_PRODUCT_ID
    mock_product_service.get.return_value = ProductOutput.from_dict({
        'id': PRODUCT_ID,
        'title': 'PRODUCT_1',
        'image': 'https://luizalabs.com/api/images/1',
        'price': 100.0
    })

@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
@patch('src.domain.interfaces.repositories.favorite_product_repository.FavoriteProductRepository')
@patch('src.application.add_product_to_favorites.IdGenerator')
@patch('src.application.add_product_to_favorites.ProductService')
def test_should_add_product_to_favorites(mock_customer_repository: CustomerRepository, 
                                  mock_favorite_product_repository: FavoriteProductRepository,
                                  mock_id_generator: IdGenerator,
                                  mock_product_service: ProductService
                                ):
    # Mocking services
    __config_default_mocks(mock_customer_repository, mock_favorite_product_repository, mock_id_generator, mock_product_service)

    favorite_product_id = AddProductToFavorites(mock_customer_repository, mock_favorite_product_repository, mock_id_generator, mock_product_service)\
        .execute(AddProductToFavoritesInput.from_dict({
            'customer_id': CUSTOMER_ID,
            'product_id': PRODUCT_ID,
        }))

    mock_customer_repository.find_by_id.assert_called_once()
    mock_favorite_product_repository.exists_product_in_customer_favorites.assert_called_once()
    mock_id_generator.generate.assert_called_once()
    mock_favorite_product_repository.add.assert_called_once()
    mock_product_service.get.assert_called_once()
    assert favorite_product_id == FAVORITE_PRODUCT_ID

    
@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
@patch('src.domain.interfaces.repositories.favorite_product_repository.FavoriteProductRepository')
@patch('src.application.add_product_to_favorites.IdGenerator')
@patch('src.application.add_product_to_favorites.ProductService')
def test_shouldnt_add_product_to_favorites_because_customer_not_exists(mock_customer_repository: CustomerRepository, 
                                  mock_favorite_product_repository: FavoriteProductRepository,
                                  mock_id_generator: IdGenerator,
                                  mock_product_service: ProductService
                                ):
    # Mocking services
    __config_default_mocks(mock_customer_repository, mock_favorite_product_repository, mock_id_generator, mock_product_service)
    # !Override default mock_customer_repository.find_by_id to return None
    mock_customer_repository.find_by_id.return_value = None

    try: 
        AddProductToFavorites(mock_customer_repository, mock_favorite_product_repository, mock_id_generator, mock_product_service)\
            .execute(AddProductToFavoritesInput.from_dict({
                'customer_id': CUSTOMER_ID,
                'product_id': PRODUCT_ID,
            }))        
    except ApplicationError as e:
        assert e.error == ApplicationErrors.NOT_FOUND
        assert str(e) == 'Customer not found'
        mock_customer_repository.find_by_id.assert_called_once()


@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
@patch('src.domain.interfaces.repositories.favorite_product_repository.FavoriteProductRepository')
@patch('src.application.add_product_to_favorites.IdGenerator')
@patch('src.application.add_product_to_favorites.ProductService')
def test_shouldnt_add_product_to_favorites_because_product_not_exists(mock_customer_repository: CustomerRepository, 
                                  mock_favorite_product_repository: FavoriteProductRepository,
                                  mock_id_generator: IdGenerator,
                                  mock_product_service: ProductService
                                ):
    # Mocking services
    __config_default_mocks(mock_customer_repository, mock_favorite_product_repository, mock_id_generator, mock_product_service)
    # !Override default mock_product_service.get to return None
    mock_product_service.get.return_value = None

    try: 
        AddProductToFavorites(mock_customer_repository, mock_favorite_product_repository, mock_id_generator, mock_product_service)\
            .execute(AddProductToFavoritesInput.from_dict({
                'customer_id': CUSTOMER_ID,
                'product_id': PRODUCT_ID,
            }))        
    except ApplicationError as e:
        assert e.error == ApplicationErrors.NOT_FOUND
        assert str(e) == 'Product not found'
        mock_customer_repository.find_by_id.assert_called_once()

@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
@patch('src.domain.interfaces.repositories.favorite_product_repository.FavoriteProductRepository')
@patch('src.application.add_product_to_favorites.IdGenerator')
@patch('src.application.add_product_to_favorites.ProductService')
def test_shouldnt_add_product_to_favorites_because_product_exists_in_customer_favorites(mock_customer_repository: CustomerRepository, 
                                  mock_favorite_product_repository: FavoriteProductRepository,
                                  mock_id_generator: IdGenerator,
                                  mock_product_service: ProductService
                                ):
    
    # Mocking services
    __config_default_mocks(mock_customer_repository, mock_favorite_product_repository, mock_id_generator, mock_product_service)
    # !Override default mock_favorite_product_repository.exists_product_in_customer_favorites to return True
    mock_favorite_product_repository.exists_product_in_customer_favorites.return_value = True

    try: 
        AddProductToFavorites(mock_customer_repository, mock_favorite_product_repository, mock_id_generator, mock_product_service)\
            .execute(AddProductToFavoritesInput.from_dict({
                'customer_id': CUSTOMER_ID,
                'product_id': PRODUCT_ID,
            }))        
    except ApplicationError as e:
        assert e.error == ApplicationErrors.CONFLICT
        assert str(e) == 'Product already exists in favorites'
        mock_customer_repository.find_by_id.assert_called_once()