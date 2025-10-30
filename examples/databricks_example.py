"""
Exemplo de uso do conector Databricks no Orion Framework.

Este exemplo demonstra como extrair dados do Databricks,
processar e salvar de volta.
"""
from typing import Any

from ...infrastructure.connectors import DatabricksConnector, DatabricksConnectorError
from ...infrastructure.config.context import OrionContext


def extract_from_databricks(context: OrionContext) -> Any:
    """
    Extrai dados de uma tabela do Databricks.

    Args:
        context: Contexto do Orion

    Returns:
        DataFrame com os dados extraídos
    """
    try:
        connector = DatabricksConnector(
            server_hostname=context.config.get("databricks_server_hostname"),
            http_path=context.config.get("databricks_http_path"),
            access_token=context.config.get("databricks_access_token"),
            catalog=context.config.get("databricks_catalog", "hive_metastore"),
            schema=context.config.get("databricks_schema", "default"),
        )

        table_name = context.config.get("source_table", "clientes_raw")
        df = connector.load(table_name=table_name)

        context.logger.info(
            "Dados extraídos do Databricks",
            extra={"rows": len(df), "table": table_name},
        )

        connector.close()
        return df

    except DatabricksConnectorError as e:
        context.logger.error(f"Erro ao extrair dados do Databricks: {e}")
        raise


def transform_data(context: OrionContext, df: Any) -> Any:
    """
    Transforma os dados extraídos.

    Args:
        context: Contexto do Orion
        df: DataFrame com dados brutos

    Returns:
        DataFrame transformado
    """
    if df is None or len(df) == 0:
        context.logger.warning("DataFrame vazio recebido para transformação")
        return df

    df.columns = [c.strip().lower() for c in df.columns]
    df = df.dropna(subset=["nome"])

    context.logger.info(
        "Dados transformados",
        extra={"rows_after": len(df)},
    )

    return df


def load_to_databricks(context: OrionContext, df: Any) -> None:
    """
    Salva dados processados de volta no Databricks.

    Args:
        context: Contexto do Orion
        df: DataFrame com dados processados
    """
    try:
        connector = DatabricksConnector(
            server_hostname=context.config.get("databricks_server_hostname"),
            http_path=context.config.get("databricks_http_path"),
            access_token=context.config.get("databricks_access_token"),
            catalog=context.config.get("databricks_catalog", "hive_metastore"),
            schema=context.config.get("databricks_schema", "default"),
        )

        table_name = context.config.get("target_table", "clientes_processed")
        mode = context.config.get("save_mode", "overwrite")

        connector.save(df, table_name=table_name, mode=mode)

        context.logger.info(
            "Dados salvos no Databricks",
            extra={"rows": len(df), "table": table_name, "mode": mode},
        )

        connector.close()

    except DatabricksConnectorError as e:
        context.logger.error(f"Erro ao salvar dados no Databricks: {e}")
        raise

