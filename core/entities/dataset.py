from abc import ABC, abstractmethod
from typing import Any

class Dataset(ABC):
    @abstractmethod
    def load(self) -> Any:
        ...

    @abstractmethod
    def save(self, data: Any) -> None:
        ...
