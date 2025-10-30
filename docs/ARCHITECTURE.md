# 🏗️ Arquitetura do Oríon Framework

Este documento detalha a arquitetura interna do Oríon Framework, baseada em Clean Architecture e princípios SOLID.

## Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER/CLI                                │
│                    orion run --module ...                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   CLI        │  │   Runner     │  │   Builder    │         │
│  │  Commands    │  │              │  │              │         │
│  │  - run       │  │  Pipeline    │  │  Pipeline    │         │
│  │  - viz       │  │  Runner      │  │  Builder     │         │
│  │  - config    │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────────────────────────────────────┐              │
│  │         Visualization (Export)               │              │
│  └──────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CORE LAYER                               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    ENTITIES                              │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │  │
│  │  │ Pipeline │  │   Node   │  │ Dataset  │              │  │
│  │  └──────────┘  └──────────┘  └──────────┘              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  INTERFACES (Contracts)                  │  │
│  │  ┌──────────────────┐  ┌──────────────────┐            │  │
│  │  │ IDataConnector   │  │    ILogger       │            │  │
│  │  │  - load()        │  │   - info()       │            │  │
│  │  │  - save()        │  │   - error()      │            │  │
│  │  └──────────────────┘  └──────────────────┘            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    USE CASES                             │  │
│  │  ┌────────────────────────────────────────────┐         │  │
│  │  │        RunPipelineUseCase                  │         │  │
│  │  │          - execute()                       │         │  │
│  │  └────────────────────────────────────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    CONNECTORS                            │  │
│  │  ┌──────────────┐  ┌──────────────────┐                │  │
│  │  │ LocalCSV     │  │ Databricks       │                │  │
│  │  │ Connector    │  │ Connector        │                │  │
│  │  └──────────────┘  └──────────────────┘                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      CATALOG                             │  │
│  │     Mapeia nomes lógicos → conectores físicos            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      LOGGING                             │  │
│  │  ┌──────────────┐  ┌──────────────────┐                │  │
│  │  │ ConsoleLogger│  │  Future: File    │                │  │
│  │  └──────────────┘  └──────────────────┘                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      CONTEXT                             │  │
│  │     OrionContext: catalog + logger + config              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      CONFIG                              │  │
│  │  ┌──────────────────┐                                   │  │
│  │  │ DatabricksConfig │                                   │  │
│  │  └──────────────────┘                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Princípios de Design

### 1. Clean Architecture

O Oríon segue os princípios de Clean Architecture de Robert C. Martin:

- **Independência de Frameworks**: O Core não depende de bibliotecas externas específicas
- **Testabilidade**: Lógica de negócio testável sem dependências externas
- **Independência de UI**: A interface CLI pode ser trocada sem afetar o Core
- **Independência de Database**: Conectores são plugáveis via interfaces

### 2. SOLID

#### Single Responsibility Principle (SRP)
- `Pipeline`: Gerencia sequência de nodes
- `Node`: Representa uma transformação
- `Catalog`: Gerencia mapeamento de datasources
- `Connector`: Implementa publish/salvar de uma fonte específica

#### Open/Closed Principle (OCP)
- Novos conectores podem ser adicionados sem modificar código existente
- Novos tipos de nodes podem ser criados via funções Python

#### Liskov Substitution Principle (LSP)
- Qualquer implementação de `IDataConnector` pode substituir outra
- Qualquer implementação de `ILogger` pode substituir outra

#### Interface Segregation Principle (ISP)
- Interfaces pequenas e focadas (`IDataConnector`, `ILogger`)
- Classes não são forçadas a implementar métodos que não usam

#### Dependency Inversion Principle (DIP)
- Alto nível (Pipeline) depende de abstrações (interfaces)
- Baixo nível (Connectors) implementa abstrações

## Fluxo de Execução Detalhado

### Passo a Passo

1. **CLI Recebe Comando**
   ```python
   # application/cli/commands.py
   orion run --module X --catalog Y
   ```

2. **Carrega Catalog**
   ```python
   catalog = DataCatalog.from_yaml("catalog.yml")
   ```

3. **Cria Context**
   ```python
   context = OrionContext(catalog=catalog, logger=ConsoleLogger())
   ```

4. **Carrega Pipeline**
   ```python
   pipeline = _load_pipeline(module_path, func_name)
   # pipeline é uma instância de Pipeline com lista de Nodes
   ```

5. **Executa Use Case**
   ```python
   runner = PipelineRunner()
   runner.run(pipeline, context)
   # Internamente chama RunPipelineUseCase.execute()
   ```

6. **Pipeline Executa Nodes (Loop)**
   ```python
   for node in pipeline.nodes:
       # 1. Preparar inputs
       inputs = []
       for input_name in node.inputs:
           if input_name in data:  # Memória
               inputs.append(data[input_name])
           else:  # Catalog
               inputs.append(context.catalog.load(input_name))
       
       # 2. Executar função do node
       outputs = node.run(context, *inputs)
       
       # 3. Armazenar outputs
       for output_name, value in zip(node.outputs, outputs):
           data[output_name] = value
           
           # 4. Auto-salvar se existe no catalog
           if context.catalog.exists(output_name):
               context.catalog.save(output_name, value)
   ```

## Design Patterns Utilizados

### Builder Pattern
- `PipelineBuilder`: Constrói pipelines de forma fluente e declarativa

### Strategy Pattern
- `IDataConnector`: Diferentes estratégias de load/save (CSV, Databricks, etc.)

### Dependency Injection
- `OrionContext`: Injeta dependências (catalog, logger) nos nodes

### Template Method
- `Pipeline.run()`: Define o algoritmo de execução, nodes implementam detalhes

### Factory Pattern
- `DataCatalog.from_yaml()`: Factory method para criar catalog

## Extensibilidade

### Adicionar Novo Conector

1. Criar classe implementando `IDataConnector`:
```python
class MyConnector(IDataConnector):
    def load(self, **kwargs) -> Any:
        # implementação
        pass
    
    def save(self, data, **kwargs) -> None:
        # implementação
        pass
```

2. Registrar no `Catalog`:
```python
catalog.connectors["my_type"] = MyConnector()
```

3. Usar no `catalog.yml`:
```yaml
my_dataset:
  type: my_type
  param1: value1
```

### Adicionar Novo Logger

1. Implementar `ILogger`
2. Instanciar em `OrionContext`

## Testabilidade

### Mocking de Dependências

```python
# Mock do catalog
mock_catalog = MagicMock()
mock_catalog.load.return_value = pd.DataFrame(...)
context = OrionContext(catalog=mock_catalog)

# Executar node
result = my_node_function(context, df)
```

### Testes de Integração

```python
# Usar catalog real com arquivos temporários
catalog = DataCatalog.from_yaml("test_catalog.yml")
context = OrionContext(catalog=catalog)
pipeline.run(context)
```

## Performance e Otimizações

### Estado em Memória
- Outputs ficam em memória durante execução
- Nodes subsequentes evitam I/O desnecessário

### Lazy Loading de Conectores
- Conectores são criados apenas quando necessário
- DatabricksConnector só conecta quando usado

### Execução Sequencial
- Garante ordem correta
- Facilita debugging
- Permite dependências entre nodes

## Segurança

### Tratamento de Credenciais
- Databricks: Arquivo `~/.orion/databricks.yml` com permissões restritas
- Nunca commitado no git
- Suporte a variáveis de ambiente

### Validação de Inputs
- Type hints obrigatórios
- Validação de schema de dados nos nodes
- Exceções claras e informativas

