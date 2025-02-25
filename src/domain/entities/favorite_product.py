
from dataclasses import asdict, dataclass
from src.domain.errors.domain_error import DomainError


@dataclass
class FavoriteProduct:

    id: str
    customer_id: str
    product_id: str
    title: str
    image: str
    price: float

    def __init__(self, id: str, customer_id: str, product_id: str, title: str, image: str, price: float):
        self.id = id
        self.customer_id = customer_id
        self.product_id = product_id
        self.title = title
        self.image = image
        self.price = price
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
        if not self.customer_id:
            errors.append('Customer id is required')
        if not self.product_id:
            errors.append('Product id is required')
        if not self.title:
            errors.append('Title is required')
        if not self.image:
            errors.append('Image is required')
        if not self.price:
            errors.append('Price is required')
        if errors: raise DomainError(", ".join(errors))
        return True