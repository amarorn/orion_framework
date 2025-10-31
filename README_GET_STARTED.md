# 🚀 Começando com Orion Framework

## ✅ Tudo Pronto para Você Começar!

Criei um **guia completo de início rápido** e um **exemplo funcional** que você pode executar agora mesmo.

---

## 📚 Documentação Criada

### 1. **GET_STARTED.md** (Raiz do projeto)
   - Guia passo a passo completo
   - Instalação
   - Primeiro exemplo
   - Troubleshooting

### 2. **docs/GUIA_DESENVOLVEDOR.md**
   - Guia completo para desenvolvedores
   - Conceitos fundamentais
   - Padrões de uso comuns
   - API Reference

### 3. **docs/COMO_FUNCIONA.md**
   - Explicação técnica detalhada
   - Arquitetura do framework
   - Fluxo de execução
   - Componentes principais

### 4. **docs/EXEMPLO_RAPIDO.md**
   - Exemplo prático rápido
   - 5 minutos para começar

---

## 🎯 Exemplo Pronto para Usar

Criei um exemplo completo em `exemplo_get_started/`:

```
exemplo_get_started/
├── pipeline.py          # Pipeline pronta
├── catalog.yml          # Catalog configurado
├── nodes/
│   ├── extract.py       # Node de extração
│   └── transform.py     # Node de transformação
└── data/
    └── raw/
        └── clientes.csv # Dados de exemplo
```

---

## ⚡ Executar o Exemplo Agora

### Passo 1: Instalar o projeto

```bash
cd /Users/joseamaro/Documents/Estudos/orion_framework
pip install -e .
```

### Passo 2: Executar o exemplo

```bash
orion run \
  --module exemplo_get_started.pipeline \
  --catalog exemplo_get_started/catalog.yml
```

### Passo 3: Ver o resultado

```bash
cat exemplo_get_started/data/processed/clientes_processados.csv
```

**Pronto!** Você verá os dados processados com a nova coluna `categoria_idade`.

---

## 📖 Como Usar o Framework

### Resumo Rápido

1. **Catalog** (`catalog.yml`): Define onde estão os dados
2. **Nodes** (`nodes/`): Funções que transformam dados
3. **Pipeline** (`pipeline.py`): Define a ordem de execução

### Fluxo

```
Catalog → Nodes → Pipeline → Execução
```

### Exemplo Mínimo

```python
# pipeline.py
from ...application.pipeline.builder import PipelineBuilder

def create_pipeline():
    builder = PipelineBuilder("minha_pipeline")
    builder.add_node(extract, inputs=[], outputs=["raw"])
    builder.add_node(transform, inputs=["raw"], outputs=["processed"])
    return builder.build()
```

---

## 🔍 Documentação Recomendada

**Para começar agora**:
1. 📘 [GET_STARTED.md](GET_STARTED.md) - Comece aqui!
2. ⚡ [docs/EXEMPLO_RAPIDO.md](docs/EXEMPLO_RAPIDO.md) - Exemplo em 5 minutos

**Para entender melhor**:
3. 🛠️ [docs/GUIA_DESENVOLVEDOR.md](docs/GUIA_DESENVOLVEDOR.md) - Guia completo
4. 🔍 [docs/COMO_FUNCIONA.md](docs/COMO_FUNCIONA.md) - Como funciona internamente

---

## 🎓 Conceitos Principais

### Node
Função Python que:
- Recebe `context: OrionContext` como primeiro parâmetro
- Recebe inputs (dados de outros nodes ou do catalog)
- Retorna outputs (dados processados)

### Pipeline
Sequência ordenada de Nodes executados sequencialmente.

### Catalog
Registro de datasources. Abstrai onde os dados estão (CSV, Databricks, etc.).

### Context
Fornece acesso a:
- `context.catalog`: Para carregar/salvar dados
- `context.logger`: Para logging
- `context.config`: Para configurações

---

## ✅ Próximos Passos

1. ✅ Execute o exemplo: `exemplo_get_started/`
2. ✅ Leia: [GET_STARTED.md](GET_STARTED.md)
3. ✅ Experimente: Modifique os nodes
4. ✅ Explore: Veja outros exemplos em `examples/`

---

## 💡 Dica

**Auto-save**: Se um output tem o mesmo nome de um dataset no catalog, ele é salvo automaticamente!

```python
# Se você tem no catalog.yml:
# clientes_processados: ...

# E na pipeline:
builder.add_node(transform, outputs=["clientes_processados"])

# O framework salva automaticamente! 🎉
```

---

**Boa codificação!** 🚀

