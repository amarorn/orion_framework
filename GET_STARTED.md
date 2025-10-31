# 🚀 Get Started - Orion Framework

Guia rápido para começar a usar o Orion Framework em **menos de 10 minutos**.

---

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip instalado
- Terminal/CLI

---

## ⚡ Instalação Rápida

### 1. Clone ou navegue até o projeto

```bash
cd orion_framework
```

### 2. Instale as dependências

```bash
pip install -e .
```

Ou instale manualmente:

```bash
pip install pandas pyyaml click
```

### 3. (Opcional) Para usar Databricks

```bash
pip install databricks-sql-connector
```

### 4. Verifique a instalação

```bash
orion --help
```

Se aparecer a ajuda do comando, está tudo OK! ✅

---

## 🎯 Primeiro Exemplo: Pipeline CSV Simples

Vamos criar uma pipeline que lê um CSV, processa os dados e salva o resultado.

### Passo 1: Criar estrutura de diretórios

```bash
mkdir -p meu_primeiro_pipeline/nodes
mkdir -p meu_primeiro_pipeline/data/raw
mkdir -p meu_primeiro_pipeline/data/processed
```

### Passo 2: Criar arquivo de dados de exemplo

Crie o arquivo `meu_primeiro_pipeline/data/raw/clientes.csv`:

```csv
nome,email,idade,cidade
João Silva,joao@email.com,30,São Paulo
Maria Santos,maria@email.com,25,Rio de Janeiro
Pedro Costa,pedro@email.com,35,Belo Horizonte
Ana Oliveira,ana@email.com,28,São Paulo
```

### Passo 3: Criar o Catalog (catalog.yml)

Crie `meu_primeiro_pipeline/catalog.yml`:

```yaml
clientes_raw:
  type: local_csv
  path: data/raw/clientes.csv

clientes_processados:
  type: local_csv
  path: data/processed/clientes_processados.csv
```

### Passo 4: Criar os Nodes

**meu_primeiro_pipeline/nodes/__init__.py**:
```python
# Arquivo vazio é OK
```

**meu_primeiro_pipeline/nodes/extract.py**:
```python
import pandas as pd
from ...infrastructure.config.context import OrionContext

def extract(context: OrionContext) -> pd.DataFrame:
    """Extrai dados do catalog."""
    df = context.catalog.load("clientes_raw")
    context.logger.info(f"Extraídos {len(df)} registros de clientes")
    return df
```

**meu_primeiro_pipeline/nodes/transform.py**:
```python
import pandas as pd
from ...infrastructure.config.context import OrionContext

def transform(context: OrionContext, df: pd.DataFrame) -> pd.DataFrame:
    """Transforma os dados."""
    context.logger.info(f"Transformando {len(df)} registros")
    
    # Normalizar colunas
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Adicionar categoria de idade
    df["categoria_idade"] = df["idade"].apply(
        lambda x: "jovem" if x < 30 else "adulto"
    )
    
    # Contar por cidade
    context.logger.info(f"Clientes por cidade: {df.groupby('cidade').size().to_dict()}")
    
    return df
```

### Passo 5: Criar a Pipeline

**meu_primeiro_pipeline/pipeline.py**:
```python
from ...application.pipeline.builder import PipelineBuilder
from .nodes.extract import extract
from .nodes.transform import transform

def create_pipeline():
    builder = PipelineBuilder("minha_primeira_pipeline")
    
    # Node 1: Extrai dados
    builder.add_node(
        extract,
        inputs=[],  # Não tem inputs
        outputs=["clientes_raw"]  # Produz este output
    )
    
    # Node 2: Transforma dados
    builder.add_node(
        transform,
        inputs=["clientes_raw"],  # Usa o output do node anterior
        outputs=["clientes_processados"]  # Produz este output
    )
    
    return builder.build()
```

### Passo 6: Executar a Pipeline

**Opção 1: Instalar o projeto em modo desenvolvimento (Recomendado)**

```bash
# Do diretório raiz do projeto orion_framework
pip install -e .
```

Depois execute:

```bash
# Do diretório raiz do projeto
orion run \
  --module exemplo_get_started.pipeline \
  --catalog exemplo_get_started/catalog.yml
```

**Opção 2: Usar PYTHONPATH**

```bash
# Do diretório raiz do projeto
PYTHONPATH=. orion run \
  --module exemplo_get_started.pipeline \
  --catalog exemplo_get_started/catalog.yml
```

### Passo 7: Verificar o Resultado

```bash
cat meu_primeiro_pipeline/data/processed/clientes_processados.csv
```

Você deve ver o CSV processado com a nova coluna `categoria_idade`! 🎉

---

## 📊 O Que Aconteceu?

1. ✅ O framework carregou o `catalog.yml`
2. ✅ Executou o node `extract`: carregou `clientes_raw` do CSV
3. ✅ Executou o node `transform`: processou os dados e adicionou coluna `categoria_idade`
4. ✅ Auto-salvou `clientes_processados` no catalog (porque está definido no catalog.yml)
5. ✅ Os dados foram salvos em `data/processed/clientes_processados.csv`

---

## 🎓 Entendendo os Conceitos

### Catalog (catalog.yml)
Define **onde estão os dados**:
- `clientes_raw`: Arquivo CSV em `data/raw/clientes.csv`
- `clientes_processados`: Arquivo CSV em `data/processed/clientes_processados.csv`

### Nodes (nodes/)
São funções Python que:
- Recebem `context: OrionContext` como primeiro parâmetro
- Podem receber inputs (dados de outros nodes ou do catalog)
- Retornam outputs (dados processados)

### Pipeline (pipeline.py)
Define a **ordem de execução** dos nodes:
1. `extract` → produz `clientes_raw`
2. `transform` → usa `clientes_raw` → produz `clientes_processados`

---

## 🔧 Executando o Exemplo Existente

O projeto já vem com um exemplo pronto! Execute:

```bash
# Do diretório raiz do projeto
PYTHONPATH=. orion run \
  --module examples.pipeline_clientes.pipeline \
  --catalog examples/pipeline_clientes/catalog.yml
```

---

## 📚 Próximos Passos

### 1. Adicionar um Node de Load

Modifique `meu_primeiro_pipeline/nodes/load.py`:

```python
import pandas as pd
from ...infrastructure.config.context import OrionContext

def load(context: OrionContext, df: pd.DataFrame) -> None:
    """Salva dados processados."""
    context.catalog.save("clientes_processados", df)
    context.logger.info(f"✅ Salvos {len(df)} registros processados")
```

E adicione na pipeline:

```python
from .nodes.load import load

# Na função create_pipeline():
builder.add_node(
    load,
    inputs=["clientes_processados"],
    outputs=[]  # Não produz outputs, só salva
)
```

### 2. Pipeline com Múltiplos Outputs

Crie um node que divide os dados:

```python
def split_by_city(context: OrionContext, df: pd.DataFrame):
    """Divide clientes por cidade."""
    sp = df[df["cidade"] == "São Paulo"]
    outros = df[df["cidade"] != "São Paulo"]
    context.logger.info(f"SP: {len(sp)}, Outros: {len(outros)}")
    return sp, outros

# Na pipeline:
builder.add_node(
    split_by_city,
    inputs=["clientes_processados"],
    outputs=["clientes_sp", "clientes_outros"]
)
```

### 3. Usar Databricks

**Configurar Databricks**:

```bash
orion databricks-config-orion
```

**Atualizar catalog.yml**:

```yaml
clientes_raw:
  type: databricks
  table: raw.clientes

clientes_processados:
  type: databricks
  table: analytics.clientes_processed
  mode: overwrite
```

Os nodes permanecem os mesmos! O framework automaticamente usa o conector apropriado.

---

## 🐛 Problemas Comuns

### Erro: "Module not found"

**Solução**: Certifique-se de estar usando `PYTHONPATH=.` antes do comando:

```bash
PYTHONPATH=. orion run --module ...
```

Ou instale o projeto em modo desenvolvimento:

```bash
pip install -e .
```

### Erro: "Dataset 'X' not found in catalog"

**Solução**: 
- Verifique se o nome está correto no `catalog.yml`
- Verifique se o caminho do arquivo está correto
- Certifique-se de que o arquivo existe

### Erro: "Input 'X' not found in memory or catalog"

**Solução**:
- Verifique se um node anterior produz esse output
- Verifique se o nome do input está correto
- Verifique a ordem dos nodes na pipeline

### Pipeline não salva dados

**Solução**:
- Verifique se o output está definido no `catalog.yml`
- O framework só auto-salva se o nome do output corresponde a uma entrada no catalog

---

## 📖 Documentação Completa

- 📘 [Guia do Desenvolvedor](docs/GUIA_DESENVOLVEDOR.md) - Guia completo de uso
- 🔍 [Como Funciona](docs/COMO_FUNCIONA.md) - Explicação técnica detalhada
- ⚡ [Exemplo Rápido](docs/EXEMPLO_RAPIDO.md) - Mais exemplos práticos
- 📚 [Documentação Principal](docs/README.md) - Referência completa

---

## ✅ Checklist de Início Rápido

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install -e .`)
- [ ] Comando `orion --help` funciona
- [ ] Estrutura de diretórios criada
- [ ] Arquivo CSV de exemplo criado
- [ ] `catalog.yml` configurado
- [ ] Nodes criados (extract, transform)
- [ ] Pipeline criada
- [ ] Pipeline executada com sucesso
- [ ] Resultado verificado

---

## 🎉 Pronto!

Agora você já sabe o básico do Orion Framework! 

Continue explorando:
- Veja exemplos em `examples/`
- Leia a documentação em `docs/`
- Experimente criar suas próprias pipelines

**Boa codificação!** 🚀

