# 🛠️ Guia de Contribuição do Oríon Framework

Este guia descreve as práticas recomendadas para colaborar com o Oríon Framework. Ele complementa a documentação técnica e garante que cada contribuição mantenha a qualidade e a consistência do projeto.

## ✅ Pré-requisitos

Antes de começar, certifique-se de:

- Ler a [documentação completa](README.md) para entender a arquitetura geral.
- Configurar o ambiente seguindo o [Guia de Início Rápido](QUICKSTART.md).
- Ter Python 3.10+ instalado e o `pip` atualizado.

## 🧱 Padrões de Arquitetura

O Oríon segue Clean Architecture e princípios SOLID. Ao propor mudanças:

- **Core (`core/`)** deve conter apenas entidades, modelos e interfaces. Evite dependências externas diretas.
- **Application (`application/`)** concentra casos de uso, serviços e CLI. Dependa apenas de contratos definidos no Core.
- **Infrastructure (`infrastructure/`)** provê implementações concretas (conectores, persistência, logging). Mantenha adapters pequenos e bem testados.

## 🧑‍💻 Estilo de Código

- Use *type hints* completos e `from __future__ import annotations` quando necessário.
- Prefira funções puras e componíveis nas pipelines.
- Adote nomes descritivos e consistentes em português para documentação e inglês para código.
- Não envolva imports em blocos `try/except`.
- Mantenha funções curtas (até ~40 linhas) e extraia responsabilidades em helpers quando necessário.

## ✅ Checklist de Pull Request

1. Adicione testes cobrindo a nova funcionalidade ou correção de bug.
2. Execute a suíte de testes localmente (`pytest`) e garanta que tudo passe.
3. Atualize a documentação relevante dentro de `docs/`.
4. Preencha a descrição da PR com contexto, screenshots (quando aplicável) e cenários de teste.
5. Solicite *review* de alguém da equipe antes do merge.

## 🧪 Testes

- Utilize `pytest` como runner padrão: `pytest -q`.
- Para features que dependem de infraestrutura externa, crie *mocks* ou *fakes* e documente os passos de validação manual.

## 📦 Versionamento e Commits

- Use commits atômicos com mensagens no formato `<tipo>: <descrição>` (ex.: `feat: adiciona conector parquet`).
- Rebase interativamente antes de abrir a PR para manter o histórico limpo.
- Não faça push de artefatos gerados (`site/`, arquivos temporários, etc.).

## 📚 Atualização da Documentação

- Cada nova feature deve ter ao menos um exemplo na pasta `examples/` ou uma nota na documentação.
- Use blocos de código com linguagem especificada para habilitar *syntax highlighting*.
- Revise a gramática e mantenha consistência visual com emojis/títulos existentes.

## 🤝 Comunicação

- Use issues do GitHub para discutir ideias maiores antes da implementação.
- Marque pessoas responsáveis quando precisar de revisão ou aprovação.
- Responda a comentários de review com contexto e, se possível, links para commits específicos.

## 📄 Licença e Créditos

Ao adicionar novos arquivos, inclua cabeçalhos de licença quando necessário e reconheça autores originais.

---

Obrigado por contribuir para o Oríon Framework! 💫
