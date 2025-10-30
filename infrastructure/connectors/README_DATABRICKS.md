# Conector Databricks para Orion Framework

Este conector permite integrar o Orion Framework com o Databricks, permitindo carregar e salvar dados de/para tabelas do Databricks.

## Instalação

Instale as dependências necessárias:

```bash
pip install databricks-sql-connector pandas
```

Ou adicione ao seu `requirements.txt`:

```
databricks-sql-connector>=2.0.0
pandas>=1.0.0
```

## Configuração

Para usar o conector, você precisa das seguintes informações do seu workspace Databricks:

- **server_hostname**: O hostname do seu workspace (ex: `workspace.cloud.databricks.com`)
- **http_path**: O HTTP path do seu SQL warehouse ou cluster
- **access_token**: Token de acesso pessoal do Databricks
- **catalog** (opcional): Nome do catalog
- **schema** (opcional): Nome do schema

## Uso Básico

### Como Node Function

```python
from ...infrastructure.connectors import DatabricksConnector
from ...infrastructure.config.context import OrionContext

def extract_from_databricks(context: OrionContext):
    """Extrai dados de uma tabela do Databricks."""
    connector = DatabricksConnector(
        server_hostname="workspace.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/your_warehouse_id",
        access_token="your_access_token",
        catalog="hive_metastore",
        schema="default"
    )
    
    df = connector.load(table_name="clientes")
    context.logger.info(f"Carregados {len(df)} registros do Databricks")
    
    return df

def save_to_databricks(context: OrionContext, df):
    """Salva dados em uma tabela do Databricks."""
    connector = DatabricksConnector(
        server_hostname="workspace.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/your_warehouse_id",
        access_token="your_access_token",
        catalog="hive_metastore",
        schema="default"
    )
    
    connector.save(df, table_name="clientes_processados", mode="overwrite")
    context.logger.info(f"Salvos {len(df)} registros no Databricks")
```

### Usando Context Manager

```python
with DatabricksConnector(
    server_hostname="workspace.cloud.databricks.com",
    http_path="/sql/1.0/warehouses/your_warehouse_id",
    access_token="your_access_token"
) as connector:
    df = connector.load(query="SELECT * FROM clientes WHERE data > '2024-01-01'")
    # Processar dados...
    connector.save(df_processed, table_name="clientes_processed", mode="append")
```

### Executar Queries Personalizadas

```python
connector = DatabricksConnector(...)
result = connector.execute_query(
    "SELECT COUNT(*) as total FROM clientes WHERE status = 'ativo'"
)
context.logger.info(f"Total de clientes ativos: {result['total'].iloc[0]}")
```

## Métodos Disponíveis

### `load(table_name=None, query=None, **kwargs)`

Carrega dados do Databricks.

**Parâmetros:**
- `table_name` (str, opcional): Nome da tabela para carregar
- `query` (str, opcional): Query SQL customizada
- `**kwargs`: Parâmetros adicionais como `limit` e `columns`

**Retorna:**
- `pd.DataFrame`: DataFrame pandas com os dados

### `save(data, table_name, mode='append', **kwargs)`

Salva dados no Databricks.

**Parâmetros:**
- `data` (pd.DataFrame): DataFrame para salvar
- `table_name` (str): Nome da tabela de destino
- `mode` (str): Modo de escrita (`'append'` ou `'overwrite'`)

### `execute_query(query, **kwargs)`

Executa uma query SQL personalizada.

**Parâmetros:**
- `query` (str): Query SQL para executar

**Retorna:**
- `Optional[pd.DataFrame]`: DataFrame com resultados ou None

## Tratamento de Erros

O conector lança `DatabricksConnectorError` em caso de falhas. Sempre trate as exceções:

```python
from ...infrastructure.connectors import DatabricksConnectorError

try:
    df = connector.load(table_name="clientes")
except DatabricksConnectorError as e:
    context.logger.error(f"Erro ao carregar dados: {e}")
    raise
```

## Observações

- O conector mantém uma conexão persistente que é reutilizada entre chamadas
- Use o método `close()` ou o context manager para fechar a conexão explicitamente
- Para operações em lote grandes, considere usar o modo `overwrite` para melhor performance

