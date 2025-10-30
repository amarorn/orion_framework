# 🚀 Guia de Início Rápido - Oríon Framework

Este guia te levará do zero a uma pipeline funcionando em poucos minutos.

## Pré-requisitos

- Python 3.8+
- pip

## Instalação

```bash
# Clone ou navegue até o diretório do projeto
cd orion_framework

# Instale dependências básicas
pip install pandas pyyaml click

# (Opcional) Se for usar Databricks
pip install databricks-sql-connector
```

## Exemplo 1: Pipeline CSV Simples

### 1. Criar estrutura de diretórios

```bash
mkdir -p meu_pipeline/nodes
mkdir -p data/raw data/processed
```

### 2. Criar catalog.yml

```yaml
# meu_pipeline/catalog.yml
clientes_raw:
  type: local_csv
  path: data/raw/clientes.csv

clientes_processados:
  type: local_csv
  path: data/processed/clientes_processed.csv
```

### 3. Criar dados de exemplo

```bash
echo "nome,email,idade
João Silva,joao@email.com,30
Maria Santos,maria@email.com,25
Pedro Costa,pedro@email.com,35" > data/raw/clientes.csv
```

### 4. Criar nodes

**meu_pipeline/nodes/extract.py**:
```python
import pandas as pd
from ...infrastructure.config.context import OrionContext

def extract(context: OrionContext) -> pd.DataFrame:
    df = context.catalog.load("clientes_raw")
    context.logger.info(f"Extraídos {len(df)} registros")
    return df
```

**meu_pipeline/nodes/transform.py**:
```python
import pandas as pd
from ...infrastructure.config.context import OrionContext

def transform(context: OrionContext, df: pd.DataFrame) -> pd.DataFrame:
    context.logger.info(f"Transformando {len(df)} registros")
    df.columns = [c.strip().lower() for c in df.columns]
    df["idade_categoria"] = df["idade"].apply(
        lambda x: "jovem" if x < 30 else "adulto"
    )
    return df
```

**meu_pipeline/nodes/load.py**:
```python
import pandas as pd
from ...infrastructure.config.context import OrionContext

def load(context: OrionContext, df: pd.DataFrame) -> None:
    context.catalog.save("clientes_processados", df)
    context.logger.info(f"Salvos {len(df)} registros processados")
```

### 5. Criar pipeline

**meu_pipeline/pipeline.py**:
```python
from ...application.pipeline.builder import PipelineBuilder
from .nodes.extract import extract
from .nodes.transform import transform
from .nodes.load import load

def create_pipeline():
    builder = PipelineBuilder("meu_pipeline_clientes")
    builder.add_node(extract, inputs=[], outputs=["clientes_raw"])
    builder.add_node(transform, inputs=["clientes_raw"], outputs=["clientes_processados"])
    builder.add_node(load, inputs=["clientes_processados"], outputs=[])
    return builder.build()
```

### 6. Executar

```bash
orion run \
  --module meu_pipeline.pipeline \
  --catalog meu_pipeline/catalog.yml
```

### 7. Verificar resultado

```bash
cat data/processed/clientes_processed.csv
```

## Exemplo 2: Pipeline com Databricks

### 1. Configurar Databricks

```bash
orion databricks-config-orion
```

Siga as instruções interativas para configurar:
- Server hostname
- HTTP path
- Access token
- (Opcional) Catalog e Schema

### 2. Criar catalog.yml

```yaml
# meu_pipeline/catalog.yml
clientes_raw:
  type: databricks
  table: raw.clientes

clientes_processados:
  type: databricks
  table: analytics.clientes_processed
  mode: overwrite
```

### 3. Usar nos nodes (mesma implementação)

```python
def extract(context: OrionContext) -> pd.DataFrame:
    df = context.catalog.load("clientes_raw")  # Carrega do Databricks!
    return df

def load(context: OrionContext, df: pd.DataFrame) -> None:
    context.catalog.save("clientes_processados", df)  # Salva no Databricks!
```

### 4. Executar (mesmo comando)

```bash
orion run \
  --module meu_pipeline.pipeline \
  --catalog meu_pipeline/catalog.yml
```

## Exemplo 3: Pipeline com Múltiplos Outputs

```python
def split_clientes(context: OrionContext, df: pd.DataFrame) -> tuple:
    """Divide clientes em ativos e inativos."""
    ativos = df[df["status"] == "ativo"]
    inativos = df[df["status"] == "inativo"]
    context.logger.info(f"Ativos: {len(ativos)}, Inativos: {len(inativos)}")
    return ativos, inativos

# No pipeline:
builder.add_node(
    split_clientes,
    inputs=["clientes"],
    outputs=["clientes_ativos", "clientes_inativos"]
)
```

## Dicas e Boas Práticas

### 1. Logging Estruturado

Sempre use `context.logger`:

```python
context.logger.info("Processando dados", extra={"count": len(df)})
context.logger.error("Erro encontrado", exc_info=True)
```

### 2. Tratamento de Erros

```python
def transform(context: OrionContext, df: pd.DataFrame) -> pd.DataFrame:
    try:
        df = df.dropna(subset=["nome"])
        return df
    except KeyError as e:
        context.logger.error(f"Coluna não encontrada: {e}")
        raise ValueError("Schema inválido") from e
```

### 3. Type Hints

Sempre use type hints:

```python
from typing import Tuple
import pandas as pd

def transform(context: OrionContext, df: pd.DataFrame) -> pd.DataFrame:
    # ...
```

### 4. Validação de Dados

```python
def transform(context: OrionContext, df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        context.logger.warning("DataFrame vazio recebido")
        return df
    
    required_columns = ["nome", "email"]
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Colunas faltando: {missing}")
    
    return df
```

## Comandos CLI Disponíveis

### Executar Pipeline

```bash
orion run --module <module_path> --catalog <catalog_path>
```

### Exportar Visualização

```bash
orion viz --module <module_path> --output pipeline.json
```

### Configurar Databricks

```bash
orion databricks-config-orion
```

## Próximos Passos

- 📖 Leia a [Documentação Completa](./README.md)
- 🏗️ Entenda a [Arquitetura](./ARCHITECTURE.md)
- 🔌 Configure o [Databricks](./DATABRICKS_SETUP.md)
- 💡 Veja mais [Exemplos](../examples/)

