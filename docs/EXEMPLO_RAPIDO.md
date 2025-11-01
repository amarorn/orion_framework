# ⚡ Exemplo Rápido - Começando em 5 minutos

Este guia mostra como criar e executar uma pipeline básica em poucos minutos.

---

## 📦 Estrutura do Projeto

Crie a seguinte estrutura:

```
exemplo_rapido/
├── pipeline.py
├── catalog.yml
├── nodes/
│   ├── __init__.py
│   ├── extract.py
│   └── transform.py
└── data/
    ├── raw/
    │   └── clientes.csv
    └── processed/
```

---

## 📝 Passo a Passo

### 1. Criar dados de exemplo

```bash
mkdir -p exemplo_rapido/data/raw exemplo_rapido/data/processed
```

Crie `exemplo_rapido/data/raw/clientes.csv`:

```csv
nome,email,idade
João Silva,joao@email.com,30
Maria Santos,maria@email.com,25
Pedro Costa,pedro@email.com,35
Ana Oliveira,ana@email.com,28
```

### 2. Criar catalog.yml

Crie `exemplo_rapido/catalog.yml`:

```yaml
clientes_raw:
  type: local_csv
  path: data/raw/clientes.csv

clientes_processados:
  type: local_csv
  path: data/processed/clientes_processados.csv
```

### 3. Criar nodes

**exemplo_rapido/nodes/__init__.py** (pode estar vazio):
```python
# Vazio é OK
```

**exemplo_rapido/nodes/extract.py**:
```python
import pandas as pd
from ...infrastructure.config.context import OrionContext

def extract(context: OrionContext) -> pd.DataFrame:
    """Extrai dados do catalog."""
    df = context.catalog.load("clientes_raw")
    context.logger.info(f"✅ Extraídos {len(df)} registros")
    return df
```

**exemplo_rapido/nodes/transform.py**:
```python
import pandas as pd
from ...infrastructure.config.context import OrionContext

def transform(context: OrionContext, df: pd.DataFrame) -> pd.DataFrame:
    """Transforma os dados."""
    context.logger.info(f"🔄 Transformando {len(df)} registros")
    
    # Normalizar colunas
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Adicionar categoria de idade
    df["categoria"] = df["idade"].apply(
        lambda x: "jovem" if x < 30 else "adulto"
    )
    
    context.logger.info(f"✅ Transformação concluída")
    return df
```

### 4. Criar pipeline

**exemplo_rapido/pipeline.py**:
```python
from ...application.pipeline.builder import PipelineBuilder
from .nodes.extract import extract
from .nodes.transform import transform

def create_pipeline():
    builder = PipelineBuilder("exemplo_rapido")
    
    builder.add_node(extract, inputs=[], outputs=["clientes_raw"])
    builder.add_node(transform, inputs=["clientes_raw"], outputs=["clientes_processados"])
    
    return builder.build()
```

### 5. Executar

```bash
cd exemplo_rapido
orion run --module exemplo_rapido.pipeline --catalog catalog.yml
```

### 6. Verificar resultado

```bash
cat data/processed/clientes_processados.csv
```

---

## 🎯 O Que Aconteceu?

1. ✅ O framework carregou o `catalog.yml`
2. ✅ Executou `extract`: carregou `clientes_raw` do CSV
3. ✅ Executou `transform`: processou os dados e adicionou coluna `categoria`
4. ✅ Auto-salvou `clientes_processados` no catalog (porque está definido no catalog.yml)
5. ✅ Os dados foram salvos em `data/processed/clientes_processados.csv`

---

## 📊 Fluxo Visual

```
┌─────────────────┐
│  catalog.yml    │  Define onde estão os dados
│                 │  - clientes_raw → data/raw/clientes.csv
│                 │  - clientes_processados → data/processed/...
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   pipeline.py   │  Define a ordem de execução
│                 │  1. extract → clientes_raw
│                 │  2. transform → clientes_processados
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   Execução      │
│                 │
│  extract()      │  Carrega CSV → retorna DataFrame
│      ↓          │
│  transform()    │  Processa DataFrame → retorna DataFrame
│      ↓          │
│  Auto-save      │  Salva no catalog (clientes_processados)
└─────────────────┘
```

---

## 🚀 Próximo Passo

Agora você pode:
- Adicionar mais nodes
- Modificar as transformações
- Usar Databricks (configure com `orion databricks-config-orion`)
- Ver mais exemplos em `examples/`

---

## ❓ Problemas Comuns

**Erro: "Module not found"**
- Certifique-se de estar no diretório correto
- Verifique que o módulo está no Python path

**Erro: "Dataset not found in catalog"**
- Verifique o nome no `catalog.yml`
- Verifique o caminho do arquivo

**Arquivo não foi salvo**
- Verifique se o output está definido no `catalog.yml`
- Verifique permissões de escrita no diretório

