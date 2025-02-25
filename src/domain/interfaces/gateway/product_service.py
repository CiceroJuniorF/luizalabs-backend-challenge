



from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

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
    async def get(self, product_id: int) -> Optional[ProductOutput]: # pragma: no cover
        pass