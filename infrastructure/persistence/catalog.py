import yaml
from typing import Dict, Any, Optional
from ..connectors.local_connector import LocalCSVConnector
from ..connectors.databricks_connector import DatabricksConnector
from ..config.databricks_config import DatabricksConfig

class DataCatalog:
    def __init__(self, entries: Dict[str, Dict[str, Any]], databricks_config_path: Optional[str] = None):
        self.entries = entries or {}
        self.databricks_config_path = databricks_config_path
        self.connectors = {
            "local_csv": LocalCSVConnector(),
        }

    @classmethod
    def from_yaml(cls, path: str, databricks_config_path: Optional[str] = None):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return cls(data, databricks_config_path=databricks_config_path)

    def exists(self, name: str) -> bool:
        return name in self.entries

    def _entry(self, name: str) -> Dict[str, Any]:
        if name not in self.entries:
            raise KeyError(f"Dataset '{name}' not found in catalog.")
        return self.entries[name]

    def _connector_for(self, entry: Dict[str, Any]):
        typ = entry.get("type")
        
        if typ == "databricks":
            if "databricks" not in self.connectors:
                try:
                    config = DatabricksConfig.load(self.databricks_config_path)
                    self.connectors["databricks"] = DatabricksConnector(
                        server_hostname=config.server_hostname,
                        http_path=config.http_path,
                        access_token=config.access_token,
                        catalog=entry.get("catalog") or config.catalog,
                        schema=entry.get("schema") or config.schema,
                    )
                except Exception as e:
                    raise KeyError(f"Erro ao criar conector Databricks: {str(e)}")
            return self.connectors["databricks"]
        
        if typ not in self.connectors:
            raise KeyError(f"Connector type '{typ}' not registered.")
        return self.connectors[typ]

    def load(self, name: str):
        entry = self._entry(name)
        connector = self._connector_for(entry)
        typ = entry["type"]
        
        if typ == "local_csv":
            return connector.load(path=entry["path"])
        elif typ == "databricks":
            table_name = entry.get("table")
            query = entry.get("query")
            return connector.load(table_name=table_name, query=query, **entry.get("options", {}))
        
        raise NotImplementedError(f"Load not implemented for type '{typ}'.")

    def save(self, name: str, data):
        entry = self._entry(name)
        connector = self._connector_for(entry)
        typ = entry["type"]
        
        if typ == "local_csv":
            import os
            os.makedirs(os.path.dirname(entry["path"]), exist_ok=True)
            return connector.save(data=data, path=entry["path"])
        elif typ == "databricks":
            table_name = entry.get("table")
            mode = entry.get("mode", "append")
            return connector.save(data=data, table_name=table_name, mode=mode)
        
        raise NotImplementedError(f"Save not implemented for type '{typ}'.")
