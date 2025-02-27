
from unittest.mock import AsyncMock, patch
from src.application.errors.application_errors_enum import ApplicationErrors
from src.domain.entities.customer import Customer
from src.domain.interfaces.id_generator import IdGenerator
from src.application.create_customer import CreateCustomer, CreateCustomerInput
from src.application.errors.application_error import ApplicationError
from src.domain.interfaces.repositories.customer_repository import CustomerRepository

NAME = "Fuu Bar"
EMAIL = "fuu.bar@mail.com"
CUSTOMER_ID = "ABC123"

def __config_default_mocks(mock_customer_repository, mock_id_generator):
    # Mocking services
    mock_customer_repository.save = AsyncMock()
    mock_customer_repository.save.return_value = CUSTOMER_ID
    mock_customer_repository.email_exists = AsyncMock()
    mock_customer_repository.email_exists.return_value = False
    mock_id_generator.generate = AsyncMock()
    mock_id_generator.generate.return_value = CUSTOMER_ID

def __create_use_case(generator, repository):
    return CreateCustomer(generator, repository)

@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
@patch('src.application.add_product_to_favorites.IdGenerator')
async def test_should_create_customer(mock_customer_repository: CustomerRepository, mock_id_generator: IdGenerator):
    __config_default_mocks(mock_customer_repository, mock_id_generator)
    create_customer = __create_use_case(generator= mock_id_generator, repository=mock_customer_repository)
    id = await create_customer.execute(CreateCustomerInput.from_dict({"name":NAME, "email":EMAIL}))
    mock_customer_repository.save.assert_called_once()
    mock_id_generator.generate.assert_called_once()
    assert id == CUSTOMER_ID


@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
@patch('src.application.add_product_to_favorites.IdGenerator')
async def test_shouldnt_create_customer_already_exists(mock_customer_repository: CustomerRepository, mock_id_generator: IdGenerator):
    __config_default_mocks(mock_customer_repository, mock_id_generator)
    # !Override default mock_customer_repository.email_exists to return False
    mock_customer_repository.email_exists.return_value = True
    try:
        create_customer = __create_use_case(generator= mock_id_generator, repository=mock_customer_repository)
        await create_customer.execute(CreateCustomerInput.from_dict({"name":NAME, "email":EMAIL}))
    except ApplicationError as e:
        assert e.error == ApplicationErrors.CONFLICT
        assert str(e) == "Customer already exists"



