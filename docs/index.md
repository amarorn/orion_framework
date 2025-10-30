# 📚 Oríon Framework - Documentação

Bem-vindo à documentação completa do **Oríon Framework**, um framework de engenharia de dados moderno baseado em Clean Architecture.

## 🎯 Sobre o Oríon

Oríon é um framework Python para construção de pipelines de dados ETL/ELT, projetado com foco em:
- **Legibilidade**: Código simples e declarativo
- **Manutenibilidade**: Arquitetura limpa e extensível
- **Observabilidade**: Logging estruturado e contextual
- **Type Safety**: Type hints obrigatórios
- **Idempotência**: Execuções determinísticas

## 📖 Documentação

### Para Iniciantes

1. **[🚀 Guia de Início Rápido](./QUICKSTART.md)**
   - Instalação
   - Primeira pipeline em 5 minutos
   - Exemplos práticos

2. **[📋 Documentação Completa](./README.md)**
   - Visão geral do framework
   - Fluxo de dados detalhado
   - Conceitos fundamentais
   - Guia de uso completo
   - API Reference

### Para Desenvolvedores

3. **[🏗️ Arquitetura](./ARCHITECTURE.md)**
   - Clean Architecture
   - Princípios SOLID
   - Design Patterns
   - Diagramas detalhados
   - Extensibilidade

4. **[📝 Developer Guidelines](../DEVELOPER_GUIDELINES.md)**
   - Padrões de código
   - Boas práticas
   - Checklist de PRs

### Integrações

5. **[🔌 Setup do Databricks](./DATABRICKS_SETUP.md)**
   - Configuração de credenciais
   - Uso com Databricks
   - Exemplos práticos

## 🔄 Fluxo de Dados (Resumo)

```
CLI → Catalog → Context → Pipeline → Nodes → Connectors → Storage
```

**Veja o [diagrama completo](./README.md#fluxo-de-dados) na documentação principal.**

## 🚀 Começando Agora

```bash
# 1. Instalar
pip install pandas pyyaml click

# 2. Criar pipeline
orion run --module seu_module.pipeline --catalog catalog.yml

# 3. Configurar Databricks (opcional)
orion databricks-config-orion
```

## 📁 Estrutura do Projeto

```
orion_framework/
├── core/              # Entidades e interfaces
├── application/       # Casos de uso, CLI, runners
├── infrastructure/    # Conectores, logging, persistência
├── examples/          # Pipelines de exemplo
└── docs/             # Esta documentação
```

## 💡 Exemplos Rápidos

### Pipeline Simples

```python
def extract(context):
    return context.catalog.load("dados_raw")

def transform(context, df):
    return df.dropna()

def create_pipeline():
    builder = PipelineBuilder("minha_pipeline")
    builder.add_node(extract, inputs=[], outputs=["dados_raw"])
    builder.add_node(transform, inputs=["dados_raw"], outputs=["dados_processados"])
    return builder.build()
```

## 🤝 Contribuindo

Consulte as [Developer Guidelines](../DEVELOPER_GUIDELINES.md) antes de contribuir.

## 📄 Licença

[Adicione informações de licença aqui]

---

**Última atualização**: 2024

