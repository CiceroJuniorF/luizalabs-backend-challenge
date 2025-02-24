from abc import ABC, abstractmethod

class IdGeneratorInterface(ABC):
    @abstractmethod
    def generate(self)-> str: # pragma: no cover 
        pass