



from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ProductOutput:
    id: int
    title: str
    image: str
    price: float

    @classmethod
    def from_dict(cls, input_value):
        return cls(**input_value)

class ProductService(ABC):
    @abstractmethod
    def get(self, product_id: int) -> ProductOutput: # pragma: no cover
        pass