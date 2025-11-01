# 🔍 Como Funciona o Orion Framework

Este documento explica **como o framework funciona internamente** de forma visual e simples.

---

## 🎯 Conceito Central

O Orion Framework executa pipelines de dados de forma **declarativa**. Você define:
- **O QUE** fazer (nodes e suas transformações)
- **ONDE** estão os dados (catalog)
- **QUAL** a ordem de execução (pipeline)

O framework se encarrega do resto: carregar dados, executar sequencialmente, gerenciar estado, salvar resultados.

---

## 📊 Arquitetura Simplificada

```
┌─────────────────────────────────────────────────────────┐
│                    VOCÊ (DESENVOLVEDOR)                  │
│                                                          │
│  1. Cria catalog.yml      → Define fontes de dados      │
│  2. Cria funções (nodes)  → Define transformações       │
│  3. Cria pipeline.py      → Define ordem de execução    │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  ORION FRAMEWORK                         │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐                  │
│  │  CLI Parser  │───▶│  Catalog     │                  │
│  └──────────────┘    │  Loader      │                  │
│                      └──────────────┘                  │
│                             │                           │
│                             ▼                           │
│  ┌──────────────┐    ┌──────────────┐                  │
│  │  Pipeline    │───▶│  Context     │                  │
│  │  Builder     │    │  Creator     │                  │
│  └──────────────┘    └──────────────┘                  │
│                             │                           │
│                             ▼                           │
│  ┌────────────────────────────────────────┐            │
│  │     Pipeline Runner (Loop Principal)   │            │
│  │                                         │            │
│  │  Para cada Node:                        │            │
│  │  1. Prepara inputs (memória ou catalog)│            │
│  │  2. Executa função do node             │            │
│  │  3. Armazena outputs em memória        │            │
│  │  4. Auto-salva se output está no cat.  │            │
│  └────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Execução Detalhado

### Fase 1: Inicialização

```
orion run --module pipeline --catalog catalog.yml
    │
    ├─▶ Carrega catalog.yml
    │   └─▶ Cria mapeamento: nome_dataset → tipo/fonte
    │
    ├─▶ Carrega pipeline.py
    │   └─▶ Chama create_pipeline()
    │       └─▶ Retorna Pipeline com lista de Nodes
    │
    └─▶ Cria OrionContext
        ├─▶ context.catalog = DataCatalog
        └─▶ context.logger = Logger
```

### Fase 2: Execução (Loop Principal)

Para cada Node na pipeline:

```
┌──────────────────────────────────────────────────┐
│ NODE: transform                                   │
│ inputs: ["clientes_raw"]                         │
│ outputs: ["clientes_processados"]                │
└──────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────┐
│ 1. PREPARA INPUTS                                │
│                                                  │
│   Para cada input "clientes_raw":               │
│   ├─ Está em data["clientes_raw"]?              │
│   │  └─▶ SIM: Usa valor em memória             │
│   │                                            │
│   └─▶ NÃO:                                     │
│       └─▶ Carrega do catalog                   │
│           ├─ Verifica tipo (local_csv/databricks)
│           ├─ Seleciona conector apropriado     │
│           └─ Executa connector.load()          │
└──────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────┐
│ 2. EXECUTA NODE                                  │
│                                                  │
│   transform(context, df_clientes_raw)           │
│   ├─ Usa context.logger para logs              │
│   ├─ Processa os dados                         │
│   └─ Retorna resultado (DataFrame)             │
└──────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────┐
│ 3. PROCESSAMENTO DE OUTPUT                       │
│                                                  │
│   Normaliza output para lista:                  │
│   - 1 output → [valor]                          │
│   - Múltiplos → [valor1, valor2, ...]          │
│                                                  │
│   Para cada output:                             │
│   ├─ Armazena em data[output_name]             │
│   └─ Se output_name existe no catalog:         │
│       └─▶ AUTO-SALVA via catalog.save()        │
└──────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────┐
│ Próximo Node...                                  │
└──────────────────────────────────────────────────┘
```

### Fase 3: Finalização

```
Todos os nodes executados
    │
    └─▶ Retorna data dict com todos os outputs
        └─▶ Fim da execução
```

---

## 🧩 Componentes Principais

### 1. Pipeline

**O que é**: Sequência ordenada de Nodes.

**Como funciona**:
```python
Pipeline.run(context)
  ├─ Inicializa data = {}
  ├─ Para cada node:
  │   ├─ Prepara inputs (data ou catalog)
  │   ├─ Executa node.run(context, *inputs)
  │   └─ Armazena outputs em data
  └─ Retorna data
```

### 2. Node

**O que é**: Função Python que transforma dados.

**Como funciona**:
```python
Node.run(context, *inputs)
  ├─ Chama node.func(context, *inputs)
  ├─ Normaliza resultado para lista
  └─ Retorna outputs normalizados
```

**Normalização**:
- Sem outputs: `[]`
- 1 output: `return df` → `[df]`
- Múltiplos: `return df1, df2` → `[df1, df2]`

### 3. Catalog

**O que é**: Registro de datasources (fontes de dados).

**Como funciona**:
```python
Catalog.load(name)
  ├─ Busca entrada no catalog.yml
  ├─ Identifica tipo (local_csv/databricks)
  ├─ Seleciona conector apropriado
  └─ Executa connector.load()

Catalog.save(name, data)
  ├─ Busca entrada no catalog.yml
  ├─ Identifica tipo
  ├─ Seleciona conector
  └─ Executa connector.save()
```

**Auto-save**: Se um output tem o mesmo nome de uma entrada no catalog, é salvo automaticamente.

### 4. Connectors

**O que são**: Implementações concretas para carregar/salvar dados.

**Tipos**:
- `LocalCSVConnector`: Carrega/salva CSV local
- `DatabricksConnector`: Carrega/salva do Databricks

**Interface**:
```python
connector.load(**params) → DataFrame
connector.save(data, **params) → None
```

### 5. Context

**O que é**: Objeto que fornece acesso a recursos do framework.

**Propriedades**:
- `context.catalog`: Acesso ao catalog (load/save)
- `context.logger`: Sistema de logging
- `context.config`: Configurações adicionais

---

## 💾 Gerenciamento de Estado

### Estado em Memória

Durante a execução, todos os outputs ficam em um dicionário `data`:

```python
data = {
    "clientes_raw": DataFrame(...),           # Output do node extract
    "clientes_processados": DataFrame(...),   # Output do node transform
    # ... outros outputs
}
```

### Resolução de Inputs

Quando um node precisa de um input:

```
1. Verifica se está em data[input_name]
   └─▶ SIM: Usa diretamente (sem I/O!)

2. Se não está em memória:
   └─▶ Carrega do catalog (via connector)
       └─▶ Armazena em data para próximos usos
```

**Benefício**: Evita recarregar dados já processados.

### Persistência Automática

Se um output tem o mesmo nome de uma entrada no catalog:

```python
# Node retorna "clientes_processados"
outputs = ["clientes_processados"]

# Se "clientes_processados" existe no catalog.yml
if catalog.exists("clientes_processados"):
    catalog.save("clientes_processados", df)  # Auto-save!
```

---

## 🔍 Exemplo de Execução Passo a Passo

Considere esta pipeline:

```python
builder.add_node(extract, inputs=[], outputs=["raw"])
builder.add_node(transform, inputs=["raw"], outputs=["processed"])
builder.add_node(load, inputs=["processed"], outputs=[])
```

**Execução**:

```
┌─────────────────────────────────────────────────────┐
│ Estado inicial: data = {}                          │
└─────────────────────────────────────────────────────┘

▼ Node 1: extract
  ├─ inputs: [] (nenhum)
  ├─ Executa: extract(context)
  │   └─▶ Carrega do catalog: "raw"
  │       └─▶ LocalCSVConnector.load("data/raw/file.csv")
  ├─ output: DataFrame
  └─ Estado: data = {"raw": DataFrame(...)}

▼ Node 2: transform
  ├─ inputs: ["raw"]
  ├─ Resolve input:
  │   └─▶ "raw" está em data["raw"]? SIM! ✅
  │       └─▶ Usa diretamente (sem I/O)
  ├─ Executa: transform(context, df_raw)
  ├─ output: DataFrame processado
  ├─ Estado: data = {"raw": ..., "processed": ...}
  └─ Auto-save: "processed" existe no catalog?
      └─▶ SIM → catalog.save("processed", df) ✅

▼ Node 3: load
  ├─ inputs: ["processed"]
  ├─ Resolve input:
  │   └─▶ "processed" está em data["processed"]? SIM! ✅
  ├─ Executa: load(context, df_processed)
  │   └─▶ Pode salvar manualmente se necessário
  └─ outputs: [] (nenhum)

┌─────────────────────────────────────────────────────┐
│ Estado final:                                      │
│ data = {                                           │
│   "raw": DataFrame(...),                           │
│   "processed": DataFrame(...)                      │
│ }                                                  │
└─────────────────────────────────────────────────────┘
```

---

## 🎓 Principais Vantagens

### 1. Declarativo
Você define **O QUE** fazer, não **COMO**. O framework gerencia execução, estado, I/O.

### 2. Reutilização de Memória
Outputs ficam em memória. Nodes subsequentes não precisam recarregar.

### 3. Auto-Persistência
Se o output está no catalog, é salvo automaticamente. Sem código extra.

### 4. Type-Safe
Type hints garantem que inputs/outputs são corretos em tempo de execução.

### 5. Observável
Logging estruturado automático através do `context.logger`.

### 6. Extensível
Fácil adicionar novos conectores (implementar `IDataConnector`).

---

## 📚 Resumo em 3 Frases

1. **Catalog**: Define onde estão os dados (CSV, Databricks, etc.)
2. **Nodes**: Funções que transformam dados, declarando inputs e outputs
3. **Pipeline**: Sequência de nodes executada automaticamente, com gerenciamento de estado e auto-persistência

O framework executa tudo de forma inteligente, otimizando I/O e simplificando seu código!

