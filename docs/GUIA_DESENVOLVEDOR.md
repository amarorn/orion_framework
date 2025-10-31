# 🛠️ Guia do Desenvolvedor - Orion Framework

Este guia explica **como funciona** e **como usar** o Orion Framework como desenvolvedor.

---

## 📋 Índice

1. [Como o Framework Funciona](#como-o-framework-funciona)
2. [Instalação e Setup](#instalação-e-setup)
3. [Estrutura de um Projeto](#estrutura-de-um-projeto)
4. [Criando sua Primeira Pipeline](#criando-sua-primeira-pipeline)
5. [Conceitos Fundamentais](#conceitos-fundamentais)
6. [Padrões de Uso Comuns](#padrões-de-uso-comuns)
7. [Comandos CLI](#comandos-cli)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Como o Framework Funciona

### Visão Geral

O **Orion Framework** é um framework de pipelines de dados que segue o padrão **ETL (Extract, Transform, Load)** de forma declarativa e type-safe.

### Fluxo de Execução

```
1. CLI executa: orion run --module pipeline --catalog catalog.yml
   ↓
2. Carrega catalog.yml (define fontes de dados)
   ↓
3. Carrega pipeline.py (define a sequência de nodes)
   ↓
4. Cria OrionContext (acesso a catalog e logger)
   ↓
5. Executa cada Node sequencialmente:
   - Carrega inputs (da memória ou do catalog)
   - Executa função do node
   - Armazena outputs na memória
   - Auto-salva no catalog (se o output existe no catalog.yml)
   ↓
6. Retorna resultados finais
```

### Princípios de Design

- **Clean Architecture**: Separação em camadas (Core, Application, Infrastructure)
- **Declarativo**: Você define O QUE fazer, não COMO fazer
- **Type-Safe**: Type hints obrigatórios
- **Idempotente**: Execuções determinísticas
- **Observável**: Logging estruturado automático

---

## ⚙️ Instalação e Setup

### 1. Instalar Dependências

```bash
# Dependências básicas
pip install pandas pyyaml click

# (Opcional) Para usar Databricks
pip install databricks-sql-connector
```

### 2. Verificar Instalação

```bash
orion --help
```

### 3. (Opcional) Configurar Databricks

Se você for usar Databricks:

```bash
orion databricks-config-orion
```

Isso criará um arquivo de configuração em `~/.orion/databricks_config.json`.

---

## 📁 Estrutura de um Projeto

### Estrutura Recomendada

```
meu_projeto/
├── pipeline.py              # Define a pipeline
├── catalog.yml              # Define os datasources
├── nodes/                   # Funções de transformação
│   ├── __init__.py
│   ├── extract.py          # Extração de dados
│   ├── transform.py        # Transformação
│   └── load.py             # Carregamento
└── data/                    # Dados (se usar local)
    ├── raw/                # Dados brutos
    └── processed/          # Dados processados
```

### Exemplo Real

```
pipeline_clientes/
├── pipeline.py
├── catalog.yml
├── nodes/
│   ├── extract_clientes.py
│   ├── transform_clientes.py
│   └── load_clientes.py
└── data/
    ├── raw/
    │   └── clientes.csv
    └── processed/
```

---

## 🚀 Criando sua Primeira Pipeline

### Passo 1: Criar o Catalog (catalog.yml)

O catalog define **onde estão os dados** e **como acessá-los**:

```yaml
# catalog.yml
clientes_raw:
  type: local_csv
  path: data/raw/clientes.csv

clientes_processados:
  type: local_csv
  path: data/processed/clientes_processed.csv
```

**Tipos disponíveis**:
- `local_csv`: Arquivo CSV local
- `databricks`: Tabela ou query do Databricks

### Passo 2: Criar os Nodes

**nodes/extract.py**:
```python
import pandas as pd
from ...infrastructure.config.context import OrionContext

def extract(context: OrionContext) -> pd.DataFrame:
    """Extrai dados do catalog."""
    df = context.catalog.load("clientes_raw")
    context.logger.info(f"Extraídos {len(df)} registros")
    return df
```

**nodes/transform.py**:
```python
import pandas as pd
from ...infrastructure.config.context import OrionContext

def transform(context: OrionContext, df: pd.DataFrame) -> pd.DataFrame:
    """Transforma os dados."""
    context.logger.info(f"Transformando {len(df)} registros")
    
    # Normalizar colunas
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Adicionar coluna calculada
    df["idade_categoria"] = df["idade"].apply(
        lambda x: "jovem" if x < 30 else "adulto"
    )
    
    return df
```

**nodes/load.py**:
```python
import pandas as pd
from ...infrastructure.config.context import OrionContext

def load(context: OrionContext, df: pd.DataFrame) -> None:
    """Salva os dados processados."""
    context.catalog.save("clientes_processados", df)
    context.logger.info(f"Salvos {len(df)} registros processados")
```

### Passo 3: Criar a Pipeline

**pipeline.py**:
```python
from ...application.pipeline.builder import PipelineBuilder
from .nodes.extract import extract
from .nodes.transform import transform
from .nodes.load import load

def create_pipeline():
    builder = PipelineBuilder("minha_primeira_pipeline")
    
    # Node 1: Extract (sem inputs, retorna clientes_raw)
    builder.add_node(
        extract,
        inputs=[],  # Não tem inputs
        outputs=["clientes_raw"]  # Produz este output
    )
    
    # Node 2: Transform (usa clientes_raw, produz clientes_processados)
    builder.add_node(
        transform,
        inputs=["clientes_raw"],  # Usa o output do node anterior
        outputs=["clientes_processados"]
    )
    
    # Node 3: Load (usa clientes_processados, não produz nada)
    builder.add_node(
        load,
        inputs=["clientes_processados"],
        outputs=[]  # Não produz outputs
    )
    
    return builder.build()
```

### Passo 4: Executar

```bash
orion run \
  --module pipeline_clientes.pipeline \
  --catalog pipeline_clientes/catalog.yml
```

### Como Funciona

1. O framework carrega o `catalog.yml`
2. Carrega a função `create_pipeline()` do módulo
3. Executa cada node na ordem definida:
   - `extract`: Carrega `clientes_raw` do catalog → retorna DataFrame
   - `transform`: Recebe o DataFrame → transforma → retorna novo DataFrame
   - `load`: Recebe o DataFrame → salva no catalog como `clientes_processados`

---

## 📚 Conceitos Fundamentais

### 1. Node (Nó)

Um **Node** é uma função Python que:
- Recebe `context: OrionContext` como primeiro parâmetro
- Recebe zero ou mais inputs como parâmetros adicionais
- Retorna um ou mais outputs

**Assinatura**:
```python
def meu_node(context: OrionContext, input1: Type1, input2: Type2) -> OutputType:
    # processamento...
    return output
```

### 2. Pipeline

Uma **Pipeline** é uma sequência ordenada de Nodes. Os nodes são executados sequencialmente, e os outputs de um node ficam disponíveis como inputs para os próximos.

### 3. Catalog

O **Catalog** é um registro de todos os datasources. Ele abstrai onde os dados estão (CSV, Databricks, etc.) e permite referenciá-los por nome.

### 4. Context

O **OrionContext** fornece:
- `context.catalog`: Para carregar/salvar dados
- `context.logger`: Para logging estruturado
- `context.config`: Para configurações adicionais

### 5. Inputs e Outputs

**Inputs**: Nomes de datasets que o node precisa (definidos no catalog ou produzidos por nodes anteriores)

**Outputs**: Nomes dos datasets que o node produz. Se um output tem o mesmo nome de um dataset no catalog, ele é **auto-salvo** automaticamente.

---

## 💡 Padrões de Uso Comuns

### Padrão 1: Extract → Transform → Load (ETL Clássico)

```python
builder.add_node(extract, inputs=[], outputs=["raw_data"])
builder.add_node(transform, inputs=["raw_data"], outputs=["processed_data"])
builder.add_node(load, inputs=["processed_data"], outputs=[])
```

### Padrão 2: Múltiplos Outputs

```python
def split_data(context: OrionContext, df: pd.DataFrame) -> tuple:
    """Divide dados em múltiplos outputs."""
    ativos = df[df["status"] == "ativo"]
    inativos = df[df["status"] == "inativo"]
    return ativos, inativos

builder.add_node(
    split_data,
    inputs=["clientes"],
    outputs=["clientes_ativos", "clientes_inativos"]
)
```

### Padrão 3: Joins e Agregações

```python
def join_dados(context: OrionContext, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """Faz join de dois datasets."""
    return df1.merge(df2, on="id", how="inner")

builder.add_node(extract_clientes, inputs=[], outputs=["clientes"])
builder.add_node(extract_pedidos, inputs=[], outputs=["pedidos"])
builder.add_node(join_dados, inputs=["clientes", "pedidos"], outputs=["clientes_com_pedidos"])
```

### Padrão 4: Validação de Dados

```python
def validar_dados(context: OrionContext, df: pd.DataFrame) -> pd.DataFrame:
    """Valida schema e dados."""
    required_cols = ["nome", "email", "idade"]
    missing = set(required_cols) - set(df.columns)
    
    if missing:
        context.logger.error(f"Colunas faltando: {missing}")
        raise ValueError(f"Schema inválido: faltam {missing}")
    
    # Validar dados
    if df.empty:
        context.logger.warning("DataFrame vazio")
        return df
    
    # Remover duplicatas
    antes = len(df)
    df = df.drop_duplicates()
    context.logger.info(f"Removidas {antes - len(df)} duplicatas")
    
    return df
```

### Padrão 5: Tratamento de Erros

```python
def processar_seguro(context: OrionContext, df: pd.DataFrame) -> pd.DataFrame:
    """Processa dados com tratamento robusto de erros."""
    try:
        df = df.dropna(subset=["nome"])
        return df
    except KeyError as e:
        context.logger.error(f"Coluna não encontrada: {e}", exc_info=True)
        raise ValueError(f"Schema inválido: {e}") from e
    except Exception as e:
        context.logger.error(f"Erro inesperado: {e}", exc_info=True)
        raise
```

### Padrão 6: Logging Estruturado

```python
def transform_com_logging(context: OrionContext, df: pd.DataFrame) -> pd.DataFrame:
    """Exemplo de logging estruturado."""
    context.logger.info("Iniciando transformação")
    context.logger.debug(f"Shape inicial: {df.shape}")
    
    antes = len(df)
    df = df.dropna()
    depois = len(df)
    
    context.logger.info(
        "Transformação concluída",
        extra={
            "linhas_antes": antes,
            "linhas_depois": depois,
            "removidas": antes - depois
        }
    )
    
    return df
```

---

## 🔧 Comandos CLI

### Executar Pipeline

```bash
orion run --module <caminho_do_modulo> --catalog <caminho_do_catalog>
```

**Exemplo**:
```bash
orion run \
  --module examples.pipeline_clientes.pipeline \
  --catalog examples/pipeline_clientes/catalog.yml
```

### Exportar Visualização

```bash
orion viz --module <caminho_do_modulo> --output <arquivo_json>
```

Gera um arquivo JSON que pode ser visualizado em ferramentas de visualização.

### Configurar Databricks

```bash
orion databricks-config-orion
```

Configura interativamente a conexão com Databricks.

---

## 🔍 Troubleshooting

### Erro: "Input 'X' not found in memory or catalog"

**Causa**: O node está tentando usar um input que não existe.

**Solução**:
1. Verifique se o input está definido no catalog.yml
2. Verifique se um node anterior produz esse output
3. Verifique a ordem dos nodes na pipeline

### Erro: "Connector type 'X' not registered"

**Causa**: Tipo de conector não suportado.

**Solução**:
1. Verifique se o tipo no catalog.yml está correto (`local_csv` ou `databricks`)
2. Para Databricks, certifique-se de ter configurado: `orion databricks-config-orion`

### Erro: "Node returned incompatible outputs"

**Causa**: O número de outputs retornados não corresponde ao declarado.

**Solução**:
1. Se o node retorna 1 output, retorne o valor diretamente: `return df`
2. Se retorna múltiplos, retorne uma tupla: `return df1, df2`
3. Verifique se o número de outputs na `add_node()` corresponde ao retorno

### Pipeline não salva dados

**Causa**: O output não está definido no catalog.yml.

**Solução**:
1. Adicione o dataset no catalog.yml
2. Ou salve manualmente no node: `context.catalog.save("nome", data)`

### Erro ao carregar do Databricks

**Causa**: Configuração incorreta ou falta de permissões.

**Solução**:
1. Verifique a configuração: `cat ~/.orion/databricks_config.json`
2. Reconfigure: `orion databricks-config-orion`
3. Verifique permissões no Databricks

---

## 📝 Checklist para Criar uma Nova Pipeline

- [ ] Criar estrutura de diretórios (`nodes/`, `data/`)
- [ ] Criar `catalog.yml` com todos os datasources
- [ ] Criar funções dos nodes em `nodes/`
- [ ] Cada função deve receber `context: OrionContext` como primeiro parâmetro
- [ ] Usar type hints em todas as funções
- [ ] Criar `pipeline.py` com `create_pipeline()`
- [ ] Adicionar nodes na ordem correta usando `builder.add_node()`
- [ ] Verificar que inputs/outputs estão corretos
- [ ] Testar localmente: `orion run --module ... --catalog ...`
- [ ] Verificar logs e resultados

---

## 🎓 Próximos Passos

- 📖 Leia a [Documentação Completa](./README.md) para detalhes avançados
- 🏗️ Entenda a [Arquitetura](./ARCHITECTURE.md) do framework
- 💡 Veja [Exemplos](../examples/) de pipelines reais
- 🔌 Configure [Databricks](./DATABRICKS_SETUP.md) se necessário

---

## 💬 Resumo Rápido

**Como funciona?**
1. Você define o catalog (onde estão os dados)
2. Você cria funções que transformam dados (nodes)
3. Você monta a pipeline declarando a ordem dos nodes
4. O framework executa tudo automaticamente

**Como usar?**
1. Crie `catalog.yml`
2. Crie funções em `nodes/`
3. Crie `pipeline.py` com `create_pipeline()`
4. Execute: `orion run --module ... --catalog ...`

**Principais conceitos**:
- **Node**: Função de transformação
- **Pipeline**: Sequência de nodes
- **Catalog**: Registro de datasources
- **Context**: Acesso a catalog e logger

