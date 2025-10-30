# 📊 Diagramas Mermaid - Oríon Framework

Este arquivo contém todos os diagramas do Oríon Framework em formato Mermaid para fácil visualização e edição.

---

## 🔄 Fluxo de Dados Completo

```mermaid
graph TB
    Start([CLI: orion run]) --> LoadConfig[Carregar catalog.yml]
    LoadConfig --> CreateContext[Criar OrionContext]
    CreateContext --> LoadPipeline[Carregar Pipeline<br/>via PipelineBuilder]
    
    LoadPipeline --> InitRunner[PipelineRunner]
    InitRunner --> UseCase[RunPipelineUseCase.execute]
    
    UseCase --> Loop{Iterar Nodes}
    
    Loop --> PrepareInputs{Preparar Inputs}
    PrepareInputs -->|Em Memória| MemCheck{Tem em data?}
    PrepareInputs -->|Do Catalog| CatalogLoad[Catalog.load]
    
    MemCheck -->|Sim| UseMemory[Usar valor em memória]
    MemCheck -->|Não| CatalogLoad
    
    CatalogLoad --> ConnectorSelect{Selecionar Connector}
    ConnectorSelect -->|local_csv| LocalConn[LocalCSVConnector]
    ConnectorSelect -->|databricks| DatabricksConn[DatabricksConnector]
    
    LocalConn --> LoadData[Carregar Dados]
    DatabricksConn --> LoadData
    
    LoadData --> ExecuteNode[Executar Node Function<br/>context, *inputs]
    ExecuteNode --> NodeLog[context.logger.info]
    
    ExecuteNode --> NormalizeOutput[Normalizar Output<br/>para tuple]
    NormalizeOutput --> StoreMemory[Armazenar em data dict]
    
    StoreMemory --> CheckCatalog{Output existe<br/>no catalog?}
    CheckCatalog -->|Sim| AutoSave[Auto-salvar via Catalog]
    CheckCatalog -->|Não| SkipSave[Pular salvamento]
    
    AutoSave --> CatalogSave[Catalog.save]
    CatalogSave --> ConnectorSelect
    
    UseMemory --> ExecuteNode
    SkipSave --> NextNode{Próximo Node?}
    
    NextNode -->|Sim| Loop
    NextNode -->|Não| ReturnResults[Retornar data dict]
    
    ReturnResults --> End([Fim])
    
    style Start fill:#e1f5ff
    style End fill:#ffe1f5
    style ExecuteNode fill:#fff5e1
    style LoadData fill:#e1ffe1
    style AutoSave fill:#f5e1ff
```

---

## 🏗️ Arquitetura em Camadas

```mermaid
graph TB
    subgraph "APPLICATION LAYER"
        CLI[CLI Commands]
        Runner[Pipeline Runner]
        Builder[Pipeline Builder]
        Viz[Visualization]
    end
    
    subgraph "CORE LAYER"
        Pipeline[Pipeline Entity]
        Node[Node Entity]
        Dataset[Dataset Entity]
        Interface[Interfaces<br/>IDataConnector<br/>ILogger]
        UseCase[RunPipelineUseCase]
    end
    
    subgraph "INFRASTRUCTURE LAYER"
        LocalConn[LocalCSV Connector]
        DBConn[Databricks Connector]
        Catalog[Data Catalog]
        Logger[Console Logger]
        Context[Orion Context]
        Config[Databricks Config]
    end
    
    CLI --> Runner
    CLI --> Builder
    Runner --> UseCase
    Builder --> Pipeline
    
    UseCase --> Pipeline
    Pipeline --> Node
    
    Node --> Interface
    Node --> Context
    
    Context --> Catalog
    Context --> Logger
    
    Catalog --> LocalConn
    Catalog --> DBConn
    
    DBConn --> Config
    
    style CLI fill:#e1f5ff
    style Pipeline fill:#fff5e1
    style Catalog fill:#e1ffe1
```

---

## 🔀 Fluxo de Execução de um Node

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant N as Node
    participant C as Context
    participant Cat as Catalog
    participant Conn as Connector
    participant Mem as Memory(data)
    
    P->>N: Preparar inputs
    loop Para cada input
        N->>Mem: Input em memória?
        alt Em memória
            Mem-->>N: Retorna valor
        else Não em memória
            N->>Cat: catalog.load(input_name)
            Cat->>Conn: Selecionar connector
            Conn->>Conn: load()
            Conn-->>Cat: DataFrame
            Cat-->>N: DataFrame
        end
    end
    
    N->>C: Executar função(context, *inputs)
    C->>C: Processar dados
    C->>C: logger.info()
    C-->>N: Retorna output(s)
    
    N->>Mem: Armazenar output em data dict
    
    alt Output existe no catalog
        N->>Cat: catalog.save(output_name, data)
        Cat->>Conn: Selecionar connector
        Conn->>Conn: save()
    end
    
    N-->>P: Node concluído
```

---

## 📦 Estrutura de Dados do Catalog

```mermaid
graph LR
    subgraph "catalog.yml"
        YAML[YAML File<br/>nome: type: ...]
    end
    
    subgraph "DataCatalog"
        Dict[entries: Dict<br/>connectors: Dict]
    end
    
    subgraph "Connectors Registry"
        Local[LocalCSVConnector]
        DB[DatabricksConnector]
    end
    
    YAML -->|from_yaml| Dict
    Dict -->|lookup| Local
    Dict -->|lookup| DB
    
    Dict -->|load/save| Local
    Dict -->|load/save| DB
```

---

## 🎯 Lifecycle de uma Pipeline

```mermaid
stateDiagram-v2
    [*] --> Definida: PipelineBuilder.build()
    
    Definida --> Contexto: Criar OrionContext
    Contexto --> Preparada: Carregar catalog.yml
    
    Preparada --> Executando: PipelineRunner.run()
    
    Executando --> ProcessandoNode: Para cada node
    ProcessandoNode --> CarregandoInputs: Preparar inputs
    CarregandoInputs --> ExecutandoFuncao: Executar função
    ExecutandoFuncao --> Persistindo: Armazenar outputs
    Persistindo --> Salvando: Auto-save (se necessário)
    Salvando --> ProcessandoNode: Próximo node
    
    ProcessandoNode --> Concluida: Todos nodes processados
    
    Concluida --> [*]
    
    ExecutandoFuncao --> Erro: Exception
    Erro --> [*]
```

---

## 🔌 Sistema de Conectores

```mermaid
classDiagram
    class IDataConnector {
        <<interface>>
        +load(**kwargs) Any
        +save(data, **kwargs) None
    }
    
    class LocalCSVConnector {
        +load(path: str) DataFrame
        +save(data, path: str) None
    }
    
    class DatabricksConnector {
        -server_hostname: str
        -http_path: str
        -access_token: str
        -connection: Connection
        +load(table_name, query) DataFrame
        +save(data, table_name, mode) None
        +execute_query(query) DataFrame
    }
    
    class DataCatalog {
        -entries: Dict
        -connectors: Dict
        +load(name: str) Any
        +save(name: str, data) None
        +exists(name: str) bool
        +_connector_for(entry) IDataConnector
    }
    
    IDataConnector <|.. LocalCSVConnector
    IDataConnector <|.. DatabricksConnector
    DataCatalog --> IDataConnector : uses
    DataCatalog --> LocalCSVConnector : creates
    DataCatalog --> DatabricksConnector : creates
```

---

## 📊 Fluxo de Dados Simplificado

```mermaid
flowchart LR
    subgraph Inputs
        CSV[CSV Files]
        DB[(Databricks Tables)]
    end
    
    subgraph Pipeline
        E[Extract Node]
        T[Transform Node]
        L[Load Node]
    end
    
    subgraph Memory
        M1[data: clientes_raw]
        M2[data: clientes_processed]
    end
    
    subgraph Outputs
        O1[CSV Output]
        O2[(Databricks Output)]
    end
    
    CSV -->|Catalog.load| E
    DB -->|Catalog.load| E
    
    E -->|returns| M1
    M1 -->|input| T
    T -->|returns| M2
    M2 -->|input| L
    
    L -->|Catalog.save| O1
    L -->|Catalog.save| O2
```

---

## 🧩 Composição de uma Pipeline

```mermaid
graph TB
    subgraph "Pipeline: ingestao_clientes"
        N1[Node: extract<br/>inputs: []<br/>outputs: [clientes_raw]]
        N2[Node: transform<br/>inputs: [clientes_raw]<br/>outputs: [clientes_tratado]]
        N3[Node: load<br/>inputs: [clientes_tratado]<br/>outputs: []]
    end
    
    N1 -->|clientes_raw| N2
    N2 -->|clientes_tratado| N3
    
    style N1 fill:#e1f5ff
    style N2 fill:#fff5e1
    style N3 fill:#ffe1f5
```

---

## 🔄 Auto-Save Mechanism

```mermaid
flowchart TD
    NodeExec[Node Executa] --> OutputRet[Retorna Output]
    OutputRet --> Normalize[Normaliza para tuple]
    Normalize --> StoreMem[Armazena em data dict]
    
    StoreMem --> CheckName{Output name<br/>existe no catalog?}
    
    CheckName -->|Sim| CheckType{Tipo de<br/>datasource?}
    CheckName -->|Não| Skip[Pular salvamento]
    
    CheckType -->|local_csv| SaveCSV[Salvar CSV]
    CheckType -->|databricks| SaveDB[Salvar Databricks]
    
    SaveCSV --> Done[Concluído]
    SaveDB --> Done
    Skip --> Done
    
    style StoreMem fill:#e1ffe1
    style CheckName fill:#fff5e1
```

---

## 📚 Relacionamento entre Entidades

```mermaid
erDiagram
    PIPELINE ||--o{ NODE : contains
    NODE ||--o{ INPUT : has
    NODE ||--o{ OUTPUT : produces
    PIPELINE ||--|| CONTEXT : uses
    CONTEXT ||--|| CATALOG : has
    CONTEXT ||--|| LOGGER : has
    CATALOG ||--o{ DATASOURCE : maps
    DATASOURCE ||--|| CONNECTOR : uses
    
    PIPELINE {
        string name
        list nodes
    }
    
    NODE {
        function func
        list inputs
        list outputs
        string name
    }
    
    CATALOG {
        dict entries
        dict connectors
    }
    
    DATASOURCE {
        string type
        dict params
    }
    
    CONTEXT {
        Catalog catalog
        Logger logger
    }
```

---

## 🚀 CLI Commands Flow

```mermaid
flowchart TD
    Start([orion CLI]) --> Command{Comando}
    
    Command -->|run| RunCmd[orion run<br/>--module X<br/>--catalog Y]
    Command -->|viz| VizCmd[orion viz<br/>--module X<br/>--output JSON]
    Command -->|databricks-config-orion| ConfigCmd[orion databricks-config-orion]
    
    RunCmd --> LoadModule[Carregar módulo]
    LoadModule --> BuildPipeline[Build Pipeline]
    BuildPipeline --> LoadCatalog[Load Catalog]
    LoadCatalog --> Execute[Executar Pipeline]
    
    VizCmd --> ExportViz[Exportar para JSON]
    
    ConfigCmd --> PromptCreds[Prompt Credenciais]
    PromptCreds --> SaveConfig[Salvar databricks.yml]
    
    Execute --> End([Resultado])
    ExportViz --> End
    SaveConfig --> End
    
    style RunCmd fill:#e1f5ff
    style ConfigCmd fill:#fff5e1
```

---

## 💾 Estado em Memória Durante Execução

```mermaid
graph TB
    subgraph "Estado Inicial"
        M0[data = {}]
    end
    
    subgraph "Após Node 1"
        M1[data = {<br/>clientes_raw: DataFrame<br/>}]
    end
    
    subgraph "Após Node 2"
        M2[data = {<br/>clientes_raw: DataFrame<br/>clientes_tratado: DataFrame<br/>}]
    end
    
    subgraph "Após Node 3"
        M3[data = {<br/>clientes_raw: DataFrame<br/>clientes_tratado: DataFrame<br/>}]
    end
    
    M0 -->|Node 1 executa| M1
    M1 -->|Node 2 lê clientes_raw| M2
    M2 -->|Node 3 lê clientes_tratado| M3
    
    style M0 fill:#ffe1f5
    style M1 fill:#e1f5ff
    style M2 fill:#e1ffe1
    style M3 fill:#fff5e1
```

---

## Como Usar Estes Diagramas

### Visualizar Online

1. **Mermaid Live Editor**: https://mermaid.live/
   - Cole qualquer diagrama do arquivo
   - Visualize e edite em tempo real

2. **GitHub/GitLab**: 
   - Diagramas Mermaid são renderizados automaticamente em markdown

3. **VS Code**:
   - Instale extensão "Markdown Preview Mermaid Support"

### Exportar como Imagem

1. No Mermaid Live Editor, use o menu de exportação
2. Escolha PNG, SVG ou PDF

### Integrar na Documentação

Os diagramas já estão integrados no `README.md`. Você pode copiar qualquer diagrama deste arquivo e usar onde necessário.

---

## Notas sobre os Diagramas

- **Fluxo de Dados Completo**: Mostra todo o processo desde CLI até finalização
- **Arquitetura em Camadas**: Visualiza as 3 camadas principais
- **Fluxo de Execução de Node**: Sequência detalhada de execução
- **Sistema de Conectores**: Classes e interfaces
- **Auto-Save Mechanism**: Como funciona o salvamento automático
- **Estado em Memória**: Como os dados fluem através da memória

Todos os diagramas são interativos e podem ser modificados conforme necessário.

