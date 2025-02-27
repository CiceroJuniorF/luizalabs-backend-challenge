from fastapi import APIRouter, Depends
from src.application.remove_customer import RemoveCustomer, RemoveCustomerInput
from src.application.update_customer import UpdateCustomer, UpdateCustomerInput
from src.dependencies import authorize, create_customer_use_case, list_customer_query, remove_customer_use_case, update_customer_use_case

from src.application.create_customer import CreateCustomer, CreateCustomerInput
from src.presentation.customer_messages import CreateCustomerRequest, CreateCustomerResponse, CustomerListResponse, UpdateCustomerRequest, UpdateCustomerResponse

router = APIRouter(prefix="/customer", tags=["Customer"])

# CREATE CUSTOMER
@router.post("/create", 
             status_code=201, 
             response_model=CreateCustomerResponse, 
             summary="Create a new customer if email not exists.",
             responses={
                    201: {"description": "Customer created successfully", "content": {"application/json": {"example": {"id": "123b27cf-d408-4695-b735-05562d8771df"}}}},
                    400: {"description": "Invalid data", "content": {"application/json": {"example": {"message": "Invalid data"}}}},
                    409: {"description": "Conflict (Customer already exists)", "content": {"application/json": {"example": {"message": "Customer already exists"}}}},
            })  
async def read_root(request: CreateCustomerRequest, 
                    authorize: bool = Depends(authorize),
                    create_customer: CreateCustomer = Depends(create_customer_use_case)) -> CreateCustomerResponse:  
    id = await create_customer.execute(CreateCustomerInput.from_dict(request.to_dict()))
    return CreateCustomerResponse.create(id=id)

# UPDATE CUSTOMER
@router.put("/update/{id}", 
             summary="Update a customer by ID",
             status_code=200, 
             response_model=UpdateCustomerResponse,
             responses={
                    200: {"description": "Ok", "content": {"application/json": {"example": {"id": "123b27cf-d408-4695-b735-05562d8771df"}}}},
                    400: {"description": "Invalid data", "content": {"application/json": {"example": {"message": "Invalid data"}}}},
                    404: {"description": "Customer not exists", "content": {"application/json": {"example": {"message": "Customer not exists"}}}},
            })
async def update_customer(id: str, 
                          update_customer_request: UpdateCustomerRequest,
                          authorize: bool = Depends(authorize), 
                          update_customer: UpdateCustomer = Depends(update_customer_use_case)) -> UpdateCustomerResponse:
    await update_customer.execute(UpdateCustomerInput.from_dict({"id":id, "name":update_customer_request.name, "email":update_customer_request.email}))
    return UpdateCustomerResponse.create(id=id)

# REMOVE CUSTOMER
@router.delete("/remove/{id}",
               status_code=204,
               summary="Remove a customer by ID",
               responses={
                    204: {"description": "Customer deleted successfully"},
                    404: {"description": "Customer not exists", "content": {"application/json": {"example": {"message": "Customer not found"}}}}
            })
async def remove_customer(id: str,
                          authorize: bool = Depends(authorize), 
                          remove_customer: RemoveCustomer = Depends(remove_customer_use_case)) -> None:
    await remove_customer.execute(RemoveCustomerInput.from_dict({"customer_id":id}))

# LIST CUSTOMERS
@router.get("/list", 
                response_model=CustomerListResponse,
                status_code=200,
                        summary="List customers with pagination",
                        responses={
                                400: {"description": "Invalid query parameters", "content": {"application/json": {"example": {"message": "Invalid query parameters"}}}},
                        })
async def list_customers(page: int = 1, size: int = 10, authorize: bool = Depends(authorize), list_customer_query = Depends(list_customer_query)):
        result = await list_customer_query.list(page, size)
        return CustomerListResponse.create(result.items, page, size, result.total_pages, result.total)

    
