



from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import List

from src.domain.entities.customer import Customer

@dataclass
class CustomerListQueryOutput:
    page: int
    size: int
    total_pages: int
    total: int
    items: List[Customer]

    def to_dict(self):
        return asdict(self)

class CustomerListQuery(ABC):
    @abstractmethod
    async def list(self, page:int = 1, size:int=10) -> CustomerListQueryOutput:
        pass


