from unittest.mock import AsyncMock, patch

from src.application.errors.application_error import ApplicationError
from src.application.errors.application_errors_enum import ApplicationErrors
from src.application.update_customer import UpdateCustomer, UpdateCustomerInput
from src.domain.entities.customer import Customer
from src.domain.errors.domain_error import DomainError
from src.domain.interfaces.repositories.customer_repository import \
    CustomerRepository

CUSTOMER_ID='eefc9802-1d7d-4aec-8190-8838ed66fbba'
customer = {
        'id': CUSTOMER_ID,
        'name': 'customer_name',
        'email': 'customer_email@mail.com'
    }
def __config_default_mocks(mock_customer_repository: CustomerRepository):
    # Mocking services
    mock_customer_repository.find_by_id = AsyncMock()
    mock_customer_repository.find_by_id.return_value = Customer.from_dict(customer)
    mock_customer_repository.save = AsyncMock()
    mock_customer_repository.save.return_value = CUSTOMER_ID



@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
async def test_should_update_customer(mock_customer_repository: CustomerRepository):
    # Mocking services
    __config_default_mocks(mock_customer_repository)

    await UpdateCustomer(mock_customer_repository) \
        .execute(UpdateCustomerInput.from_dict({
            'id': CUSTOMER_ID,
            'name': 'new_name',
            'email': 'new_mail@mail.com'
        }))
    customer_cp = customer.copy()
    customer_cp['name'] = 'new_name'
    customer_cp['email'] = 'new_mail@mail.com'
    mock_customer_repository.find_by_id.assert_called_once()
    mock_customer_repository.find_by_id.assert_called_with(CUSTOMER_ID)
    mock_customer_repository.save.assert_called_once()
    mock_customer_repository.save.assert_called_with(Customer.from_dict(customer_cp))
    

@patch('src.domain.interfaces.repositories.customer_repository.CustomerRepository')
async def test_shouldnt_update_customer_because_invalid_email(mock_customer_repository: CustomerRepository):
    # Mocking services
    __config_default_mocks(mock_customer_repository)

    try: 
        await UpdateCustomer(mock_customer_repository) \
            .execute(UpdateCustomerInput.from_dict({
                'id': CUSTOMER_ID,
                'name': 'new_name',
                'email': 'new_invalid_mail.com'
            }))
    except DomainError as e:
        assert str(e) == "Invalid email"
        mock_customer_repository.find_by_id.assert_called_once()
        mock_customer_repository.find_by_id.assert_called_with(CUSTOMER_ID)
        mock_customer_repository.save.assert_not_called()

