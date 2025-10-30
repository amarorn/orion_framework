from typing import Any, Optional
import pandas as pd
from databricks import sql
from databricks.sql.client import Connection

from ...core.interfaces.IDataConnector import IDataConnector


class DatabricksConnectorError(Exception):
    """Exceção customizada para erros do conector Databricks."""

    pass


class DatabricksConnector(IDataConnector):
    """
    Conector para Databricks usando databricks-sql-connector.

    Permite carregar e salvar dados de/para tabelas do Databricks,
    bem como executar queries SQL personalizadas.
    """

    def __init__(
        self,
        server_hostname: str,
        http_path: str,
        access_token: str,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
    ) -> None:
        """
        Inicializa o conector Databricks.

        Args:
            server_hostname: Hostname do workspace Databricks (ex: workspace.cloud.databricks.com)
            http_path: HTTP path do SQL warehouse/cluster
            access_token: Token de acesso do Databricks
            catalog: Catalog opcional (default: None)
            schema: Schema opcional (default: None)
        """
        self.server_hostname = server_hostname
        self.http_path = http_path
        self.access_token = access_token
        self.catalog = catalog
        self.schema = schema
        self._connection: Optional[Connection] = None

    def _get_connection(self) -> Connection:
        """
        Obtém ou cria uma conexão com o Databricks.

        Returns:
            Connection: Conexão ativa com o Databricks

        Raises:
            DatabricksConnectorError: Se houver erro ao estabelecer conexão
        """
        if self._connection is None:
            try:
                self._connection = sql.connect(
                    server_hostname=self.server_hostname,
                    http_path=self.http_path,
                    access_token=self.access_token,
                )
            except Exception as e:
                raise DatabricksConnectorError(
                    f"Falha ao conectar com Databricks: {str(e)}"
                ) from e

        return self._connection

    def _build_full_table_name(self, table_name: str) -> str:
        """
        Constrói o nome completo da tabela com catalog e schema se especificados.

        Args:
            table_name: Nome da tabela

        Returns:
            str: Nome completo da tabela (catalog.schema.table ou schema.table ou table)
        """
        parts = []
        if self.catalog:
            parts.append(self.catalog)
        if self.schema:
            parts.append(self.schema)
        parts.append(table_name)
        return ".".join(parts)

    def load(
        self,
        table_name: Optional[str] = None,
        query: Optional[str] = None,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Carrega dados do Databricks.

        Args:
            table_name: Nome da tabela para carregar (opcional se query fornecida)
            query: Query SQL customizada (opcional se table_name fornecido)
            **kwargs: Parâmetros adicionais (limit, columns, etc.)

        Returns:
            pd.DataFrame: DataFrame pandas com os dados carregados

        Raises:
            DatabricksConnectorError: Se houver erro ao carregar dados
            ValueError: Se nem table_name nem query forem fornecidos
        """
        if not table_name and not query:
            raise ValueError(
                "É necessário fornecer 'table_name' ou 'query' para carregar dados"
            )

        connection = self._get_connection()
        cursor = connection.cursor()

        try:
            if query:
                sql_query = query
            else:
                full_table_name = self._build_full_table_name(table_name)
                limit = kwargs.get("limit", None)
                columns = kwargs.get("columns", "*")

                sql_query = f"SELECT {columns} FROM {full_table_name}"
                if limit:
                    sql_query += f" LIMIT {limit}"

            cursor.execute(sql_query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            df = pd.DataFrame(results, columns=columns)
            return df

        except Exception as e:
            raise DatabricksConnectorError(
                f"Erro ao carregar dados do Databricks: {str(e)}"
            ) from e
        finally:
            cursor.close()

    def save(
        self,
        data: pd.DataFrame,
        table_name: str,
        mode: str = "append",
        **kwargs: Any,
    ) -> None:
        """
        Salva dados no Databricks usando INSERT statements.

        Args:
            data: DataFrame pandas para salvar
            table_name: Nome da tabela de destino
            mode: Modo de escrita ('append' ou 'overwrite')
            **kwargs: Parâmetros adicionais ignorados

        Raises:
            DatabricksConnectorError: Se houver erro ao salvar dados
            ValueError: Se mode não for 'append' ou 'overwrite'
        """
        if mode not in ["append", "overwrite"]:
            raise ValueError("Mode deve ser 'append' ou 'overwrite'")

        if data.empty:
            return

        connection = self._get_connection()
        cursor = connection.cursor()
        full_table_name = self._build_full_table_name(table_name)

        try:
            if self.catalog:
                cursor.execute(f"USE CATALOG {self.catalog}")
            if self.schema:
                cursor.execute(f"USE SCHEMA {self.schema}")

            if mode == "overwrite":
                cursor.execute(f"DROP TABLE IF EXISTS {full_table_name}")

            columns_str = ",".join(data.columns)
            placeholders = ",".join(["?" for _ in range(len(data.columns))])
            insert_query = (
                f"INSERT INTO {full_table_name} ({columns_str}) VALUES ({placeholders})"
            )

            rows = data.values.tolist()
            cursor.executemany(insert_query, rows)
            connection.commit()

        except Exception as e:
            raise DatabricksConnectorError(
                f"Erro ao salvar dados no Databricks: {str(e)}"
            ) from e
        finally:
            cursor.close()

    def execute_query(self, query: str, **kwargs: Any) -> Optional[pd.DataFrame]:
        """
        Executa uma query SQL personalizada e retorna resultados como DataFrame.

        Args:
            query: Query SQL para executar
            **kwargs: Parâmetros adicionais ignorados

        Returns:
            Optional[pd.DataFrame]: DataFrame com resultados ou None se não houver resultados

        Raises:
            DatabricksConnectorError: Se houver erro ao executar query
        """
        connection = self._get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            if cursor.description:
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(results, columns=columns)
            return None

        except Exception as e:
            raise DatabricksConnectorError(
                f"Erro ao executar query no Databricks: {str(e)}"
            ) from e
        finally:
            cursor.close()

    def close(self) -> None:
        """Fecha a conexão com o Databricks."""
        if self._connection:
            try:
                self._connection.close()
                self._connection = None
            except Exception:
                pass

    def __enter__(self) -> "DatabricksConnector":
        """Suporte para context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Cleanup ao sair do context manager."""
        self.close()
