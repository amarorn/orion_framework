from typing import Optional, Dict, Any
import os
import yaml
from pathlib import Path


class DatabricksConfigError(Exception):
    """Exceção para erros de configuração do Databricks."""

    pass


class DatabricksConfig:
    """
    Gerenciador de configuração centralizada do Databricks.

    Carrega configurações de um arquivo databricks.yml ou de variáveis de ambiente.
    """

    DEFAULT_CONFIG_PATH = Path.home() / ".orion" / "databricks.yml"

    def __init__(
        self,
        server_hostname: Optional[str] = None,
        http_path: Optional[str] = None,
        access_token: Optional[str] = None,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
    ) -> None:
        """
        Inicializa configuração do Databricks.

        Args:
            server_hostname: Hostname do workspace
            http_path: HTTP path do warehouse/cluster
            access_token: Token de acesso
            catalog: Catalog opcional
            schema: Schema opcional
        """
        self.server_hostname = server_hostname
        self.http_path = http_path
        self.access_token = access_token
        self.catalog = catalog
        self.schema = schema

    @classmethod
    def from_file(cls, config_path: Optional[str] = None) -> "DatabricksConfig":
        """
        Carrega configuração de um arquivo YAML.

        Args:
            config_path: Caminho do arquivo de configuração. Se None, usa o padrão.

        Returns:
            DatabricksConfig: Instância configurada

        Raises:
            DatabricksConfigError: Se houver erro ao carregar configuração
        """
        if config_path is None:
            config_path = str(cls.DEFAULT_CONFIG_PATH)

        config_file = Path(config_path)

        if not config_file.exists():
            raise DatabricksConfigError(
                f"Arquivo de configuração não encontrado: {config_path}"
            )

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            return cls(
                server_hostname=data.get("server_hostname"),
                http_path=data.get("http_path"),
                access_token=data.get("access_token"),
                catalog=data.get("catalog"),
                schema=data.get("schema"),
            )
        except Exception as e:
            raise DatabricksConfigError(
                f"Erro ao carregar configuração: {str(e)}"
            ) from e

    @classmethod
    def from_env(cls) -> "DatabricksConfig":
        """
        Carrega configuração de variáveis de ambiente.

        Returns:
            DatabricksConfig: Instância configurada
        """
        return cls(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_ACCESS_TOKEN"),
            catalog=os.getenv("DATABRICKS_CATALOG"),
            schema=os.getenv("DATABRICKS_SCHEMA"),
        )

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "DatabricksConfig":
        """
        Carrega configuração tentando primeiro arquivo, depois variáveis de ambiente.

        Args:
            config_path: Caminho do arquivo de configuração (opcional)

        Returns:
            DatabricksConfig: Instância configurada

        Raises:
            DatabricksConfigError: Se configuração não for encontrada
        """
        if config_path:
            return cls.from_file(config_path)

        try:
            return cls.from_file()
        except DatabricksConfigError:
            config = cls.from_env()
            if not config.server_hostname or not config.http_path or not config.access_token:
                raise DatabricksConfigError(
                    "Configuração do Databricks não encontrada. "
                    "Configure via arquivo ~/.orion/databricks.yml ou variáveis de ambiente."
                )
            return config

    def save(self, config_path: Optional[str] = None) -> None:
        """
        Salva configuração em um arquivo YAML.

        Args:
            config_path: Caminho do arquivo. Se None, usa o padrão.

        Raises:
            DatabricksConfigError: Se houver erro ao salvar
        """
        if config_path is None:
            config_path = str(self.DEFAULT_CONFIG_PATH)

        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "server_hostname": self.server_hostname,
            "http_path": self.http_path,
            "access_token": self.access_token,
        }

        if self.catalog:
            data["catalog"] = self.catalog
        if self.schema:
            data["schema"] = self.schema

        try:
            with open(config_file, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

        except Exception as e:
            raise DatabricksConfigError(f"Erro ao salvar configuração: {str(e)}") from e

    def validate(self) -> None:
        """
        Valida se a configuração está completa.

        Raises:
            DatabricksConfigError: Se configuração estiver incompleta
        """
        if not self.server_hostname:
            raise DatabricksConfigError("server_hostname não configurado")
        if not self.http_path:
            raise DatabricksConfigError("http_path não configurado")
        if not self.access_token:
            raise DatabricksConfigError("access_token não configurado")

    def to_dict(self) -> Dict[str, Any]:
        """Retorna configuração como dicionário."""
        return {
            "server_hostname": self.server_hostname,
            "http_path": self.http_path,
            "access_token": self.access_token,
            "catalog": self.catalog,
            "schema": self.schema,
        }

