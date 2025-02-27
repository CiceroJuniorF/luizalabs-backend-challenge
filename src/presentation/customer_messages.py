from dataclasses import asdict, dataclass
from typing import List

from pydantic import BaseModel, Field

from src.domain.entities.customer import Customer


@dataclass
class CreateCustomerRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=300, example="Name SecondName")
    email: str = Field(..., pattern=".*@.*", example="mail@mail.com")

    def to_dict(self):
        return asdict(self)

@dataclass
class CreateCustomerResponse():
    id: str
    def __init__(self, id):
        self.id = id
    
    @classmethod
    def create(self, id: str):
        return CreateCustomerResponse(id=id)
    
@dataclass
class UpdateCustomerRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=300, example="Name SecondName")
    email: str = Field(..., pattern=".*@.*", example="mail@mail.com")

    def to_dict(self):
        return asdict(self)

@dataclass
class UpdateCustomerResponse():
    id: str
    def __init__(self, id):
        self.id = id
    
    @classmethod
    def create(self, id: str):
        return UpdateCustomerResponse(id=id)

@dataclass
class CustomerListResponse():
    page: int
    size: int
    total_pages: int
    total: int
    items: List[Customer]

    @classmethod
    def create(self, items: List[Customer], page: int, size: int, total_pages: int, total: int):
        return CustomerListResponse(items=items, page=page, size=size, total_pages=total_pages, total=total)