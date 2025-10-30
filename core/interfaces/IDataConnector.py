from abc import ABC, abstractmethod
from typing import Any

class IDataConnector(ABC):
    @abstractmethod
    def load(self, **kwargs) -> Any: ...
    @abstractmethod
    def save(self, data, **kwargs) -> None: ...
