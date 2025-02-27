from dataclasses import asdict, dataclass

from pydantic import BaseModel, Field


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
