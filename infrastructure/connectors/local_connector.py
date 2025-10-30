from ...core.interfaces.IDataConnector import IDataConnector
import pandas as pd
from typing import Any

class LocalCSVConnector(IDataConnector):
    def load(self, path: str, **kwargs) -> Any:
        return pd.read_csv(path, **kwargs)

    def save(self, data, path: str, **kwargs) -> None:
        if hasattr(data, "to_csv"):
            data.to_csv(path, index=False, **kwargs)
        else:
            raise TypeError("LocalCSVConnector expects a pandas-like object with .to_csv")
