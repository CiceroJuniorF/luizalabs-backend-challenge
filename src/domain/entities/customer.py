
from dataclasses import asdict, dataclass

from src.domain.errors.domain_error import DomainError

@dataclass
class Customer:
    
    id: str
    name: str
    email: str

    def __init__(self, id: str,  name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
        self.__validate()
    
    @classmethod
    def from_dict(cls, input_value):
        instance =  cls(**input_value)
        instance.__validate()
        return instance

    def to_dict(self) -> dict:
        return asdict(self)
    
    def __validate(self) -> bool:
        errors = []
        if not self.id:
            errors.append('Id is required')
        if not self.name:
            errors.append('Name is required')
        if not self.email:
            errors.append('Email is required')
        elif self.email.find('@') == -1:
            errors.append('Invalid email')
        if errors: raise DomainError(", ".join(errors))
        return True