# 🚀 Guia de Início Rápido — Orion Framework

Este guia coloca o Orion Framework em funcionamento em minutos. Você aprenderá a instalar o projeto, executar a pipeline de exemplo e construir a sua própria usando os componentes principais (`Pipeline`, `Node`, `DataCatalog` e `OrionContext`).

---

## 1. Pré-requisitos

- Python 3.8+ com `pip`
- Acesso ao terminal
- (Opcional) Ambiente virtual para isolar dependências

> Dica: em macOS/Linux, execute `python3 --version` e `pip --version` para validar o ambiente.

---

## 2. Instalação e Configuração

1. Navegue até a pasta do projeto:
   ```bash
   cd /Users/joseamaro/Documents/Estudos/orion_framework
   ```
2. (Opcional) Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. Instale o framework em modo desenvolvimento:
   ```bash
   pip install -e .
   ```
4. Confirme se o CLI está acessível:
   ```bash
   orion --help
   ```
   A exibição do menu de ajuda indica que tudo está configurado ✅

Dependências adicionais:
- `pip install databricks-sql-connector` para habilitar conectores Databricks.
- Consulte `requirements_databricks.txt` para pacotes opcionais.

---

## 3. Estrutura Essencial

```
core/            # Entidades de domínio e regras de negócio
application/     # Builders, runner e comandos CLI
infrastructure/  # Catálogo, conectores e configuração
examples/        # Pipelines de referência
exemplo_get_started/  # Tutorial completo com dados e nodes
docs/            # Documentação detalhada
run_tests.py     # Smoke tests pós-instalação
test_pipeline.py # Teste funcional end-to-end
```

Respeite essa separação em camadas ao criar novos módulos ou pipelines.

---

## 4. Execute o Exemplo Pronto

Comece rodando a pipeline disponibilizada em `exemplo_get_started/`:

```bash
orion run \
  --module exemplo_get_started.pipeline \
  --catalog exemplo_get_started/catalog.yml
```

O arquivo `data/processed/clientes_processados.csv` será gerado com uma nova coluna `categoria_idade`. Para executar sem instalar em modo editável, exporte o projeto diretamente:

```bash
PYTHONPATH=. orion run \
  --module exemplo_get_started.pipeline \
  --catalog exemplo_get_started/catalog.yml
```

---

## 5. Crie Sua Primeira Pipeline

1. Estruture o diretório:
   ```bash
   mkdir -p meu_pipeline/{nodes,data/raw,data/processed}
   ```
2. Defina o `catalog.yml` mapeando datasets:
   ```yaml
   clientes_raw:
     type: local_csv
     path: data/raw/clientes.csv
   clientes_processados:
     type: local_csv
     path: data/processed/clientes_processados.csv
   ```
3. Implemente nodes em `nodes/` usando `OrionContext` para carregar e salvar dados (veja exemplos em `exemplo_get_started/nodes`).
4. Monte a pipeline com `PipelineBuilder` em `meu_pipeline/pipeline.py`, declarando inputs/outputs coerentes com o catalog.
5. Execute:
   ```bash
   orion run --module meu_pipeline.pipeline --catalog meu_pipeline/catalog.yml
   ```

O autosave implementado em `core/entities/pipeline.py` garante que outputs com nomes presentes no catalog sejam persistidos automaticamente.

---

## 6. Valide com Testes

Rode os testes rápidos antes de abrir PRs ou compartilhar alterações:

```bash
python run_tests.py      # Verifica imports e componentes críticos
python test_pipeline.py  # Exercita uma pipeline end-to-end com logs
```

Para novas funcionalidades, acrescente testes unitários nas pastas correspondentes (`core`, `application`, `infrastructure`) utilizando fixtures determinísticas e mocks para conectores externos.

---

## 7. Próximos Passos

- Leia `docs/GUIA_DESENVOLVEDOR.md` e `docs/COMO_FUNCIONA.md` para aprofundar conceitos.
- Explore `docs/EXEMPLO_RAPIDO.md` e `examples/` para mais receitas de pipelines.
- Configure `orion databricks-config-orion` quando precisar falar com Databricks e atualize o `catalog.yml` com `type: databricks`.
- Consulte `GITFLOW_SUMMARY.md` para alinhar fluxo de trabalho (branches, commits e PRs).

Em caso de erro (`ModuleNotFoundError`, por exemplo), confirme que o ambiente virtual está ativo, reinstale com `pip install -e .` e utilize `PYTHONPATH=.` ao executar módulos diretamente.

Bom desenvolvimento! 💡
