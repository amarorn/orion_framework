# Repository Guidelines

## Project Structure & Module Organization
`core/` concentra entidades, interfaces e casos de uso e deve permanecer livre de dependências externas. `application/` expõe a orquestração de pipelines, builders e CLI; `infrastructure/` reúne conectores, persistência e configuração (`infrastructure/config/context.py`). Materiais de apoio estão em `docs/`, exemplos em `examples/` e no guia completo `exemplo_get_started/`. Use `run_tests.py` como checagem rápida após instalação.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate`: cria o ambiente isolado padrão.
- `pip install -e .`: instala o framework em modo editável e habilita o CLI `orion`.
- `python run_tests.py`: roda smoke tests e verifica imports essenciais.
- `python test_pipeline.py`: executa o teste funcional end-to-end com logs ricos.
- `orion run --module exemplo_get_started.pipeline --catalog exemplo_get_started/catalog.yml`: demonstra pipeline pronta com catalog configurado.

## Coding Style & Naming Conventions
Código Python segue PEP 8, com indentação de 4 espaços e linhas até 100 caracteres. Classes usam `PascalCase`, funções e variáveis `snake_case`, constantes em MAIÚSCULAS. Tipagens explícitas e docstrings concisas são preferidas; consulte `core/entities/pipeline.py` e `application/pipeline/builder.py`. Prefira `context.logger` para mensagens operacionais e mantenha comandos CLI agrupados em `application/cli`.

## Testing Guidelines
Valide mudanças com `python run_tests.py` antes de abrir PR. Amplie cobertura com testes unitários específicos por camada (conectores exigem mocks de serviços externos) e adicione cenários funcionais seguindo `test_pipeline.py` quando a integração de nodes precisar de verificação end-to-end. Prefira fixtures determinísticos e utilize `DataCatalog` com caminhos temporários para evitar efeitos colaterais. Relate comandos executados e resultados no PR.

## Commit & Pull Request Guidelines
Adote as convenções vistas em `feature/*`: prefixe commits com `feat:`, `fix:`, `docs:`, `refactor:` etc., descrevendo o efeito no imperativo. Trabalhe em branches derivados de `develop` (`feature/<nome-curto>`) e mantenha PRs focados. Cada PR deve trazer descrição objetiva, referência a issues, evidências dos testes executados e artefatos úteis (logs ou screenshots do CLI). Aguarde revisão de pares das camadas tocadas antes de mesclar.

## Configuration & Connector Notes
Guarde segredos fora do repositório: aplique variáveis de ambiente e arquivos `.env` ignorados pelo Git para credenciais de conectores. Defina datasets adicionais em `catalog.yml` mantendo aliases alinhados aos outputs dos nodes para tirar proveito do autosave em `core/entities/pipeline.py`. Documente dependências opcionais (como Databricks) em `requirements_databricks.txt` ou notas dentro de `docs/`.
