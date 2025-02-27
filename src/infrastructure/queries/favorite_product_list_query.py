



from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import List

from src.domain.entities.customer import Customer
from src.domain.entities.favorite_product import FavoriteProduct

@dataclass
class FavoriteProductListQueryOutput:
    page: int
    size: int
    total_pages: int
    total: int
    items: List[FavoriteProduct]

    def to_dict(self):
        return asdict(self)

class FavoriteProductListQuery(ABC):
    @abstractmethod
    async def list(self, customer_id: str, page:int = 1, size:int=10) -> FavoriteProductListQueryOutput:
        pass


