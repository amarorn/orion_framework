# 🧾 Handoff Analista → Engenharia (SQL First)

Este roteiro ajuda o analista a abrir uma demanda para o time de engenharia dentro do Orion Framework, mantendo a conversa em “idioma SQL” e garantindo que a equipe técnica tenha tudo o que precisa para criar nodes ou ajustar o catálogo.

---

## 1. Ficha de Contexto

| Campo | Descrição / Exemplo |
| --- | --- |
| Pergunta de negócio | “Qual o faturamento mensal por região considerando apenas clientes ativos?” |
| Stakeholders | Equipe Comercial LATAM |
| Frequência desejada | Mensal (D+2) |
| Dataset(s) alvo | `vendas_mensais`, `clientes_dim` |
| Granularidade | Mês x Região |
| Restrições/conformidades | Excluir pedidos cancelados; moeda BRL |
| Exemplo de linha | `2024-05`, `LATAM`, `125000.00` |

> **Dica:** anexar CSV curto ou captura da visão esperada ajuda a validar campos calculados.

---

## 2. Requisitos → SQL (esboço)

Preencha com a melhor aproximação da query final. Use aliases do catálogo quando souber e marque pontos em aberto.

```sql
WITH pedidos_filtrados AS (
    SELECT
        p.pedido_id,
        p.data_pedido,
        p.valor_total,
        c.regiao
    FROM {{ catalog.vendas_mensais }} AS p
    INNER JOIN {{ catalog.clientes_dim }} AS c
        ON p.cliente_id = c.cliente_id
    WHERE
        p.status = 'concluido'
        -- TODO: confirmar se pedidos com devolução parcial entram
),
faturamento AS (
    SELECT
        DATE_TRUNC('month', data_pedido) AS mes,
        regiao,
        SUM(valor_total) AS receita
    FROM pedidos_filtrados
    GROUP BY 1, 2
)
SELECT
    mes,
    regiao,
    receita
FROM faturamento
ORDER BY mes DESC, regiao;
```

Checklist rápido:

- [ ] Todos os filtros obrigatórios foram mapeados?
- [ ] Campos calculados possuem lógica descrita/comentada?
- [ ] Existem dúvidas ressaltadas com `TODO`?
- [ ] A ordenação e o limite de linhas estão claros?

---

## 3. Matriz de Impacto

| Output | Origem (Catalog / Novo) | Transformação / Observações | Responsável |
| --- | --- | --- | --- |
| `mes` | `vendas_mensais` (catalog) | `DATE_TRUNC('month', data_pedido)` | Engenharia |
| `regiao` | `clientes_dim` (catalog) | Join via `cliente_id` | Engenharia / Governança Clientes |
| `receita` | `vendas_mensais` (catalog) | Soma de `valor_total` após filtros | Engenharia |

Use esta tabela para sinalizar campos que exigem criação de novos conectores, ajuste de catálogo ou validação com outro time.

---

## 4. Cenário de Validação

Descreva como comprovar que o resultado está correto.

- **Teste mínimo:** comparar receita de abril/2024 com relatório financeiro oficial (diferença máxima 1%).
- **Contagem esperada:** número de regiões deve coincidir com tabela `regioes_dim` (5 linhas).
- **Campo derivado:** `receita` deve ser sempre >= 0.

---

## 5. Exemplo de Mapeamento para Orion

### 5.1. Ajustes no catálogo (se necessário)

```yaml
# catalog.yml
vendas_mensais:
  type: databricks
  table: bronze.vendas_mensais

clientes_dim:
  type: databricks
  table: silver.clientes_dim

faturamento_regional:
  type: databricks
  table: gold.faturamento_regional
```

### 5.2. Node em Python

```python
from orion.application.pipeline.context import OrionContext
import pandas as pd

def gerar_faturamento_regional(context: OrionContext) -> pd.DataFrame:
    vendas = context.catalog.load("vendas_mensais")
    clientes = context.catalog.load("clientes_dim")

    dados = (
        vendas.merge(clientes[["cliente_id", "regiao"]], on="cliente_id", how="inner")
        .query("status == 'concluido'")
    )

    # TODO: confirmar regra para devoluções parciais
    resultado = (
        dados.assign(mes=lambda df: df["data_pedido"].dt.to_period("M").dt.to_timestamp())
        .groupby(["mes", "regiao"], as_index=False)["valor_total"]
        .sum()
        .rename(columns={"valor_total": "receita"})
        .sort_values(["mes", "regiao"], ascending=[False, True])
    )

    return resultado
```

### 5.3. Registro na pipeline

```python
builder.add_node(
    gerar_faturamento_regional,
    inputs=["vendas_mensais", "clientes_dim"],
    outputs=["faturamento_regional"],
)
```

---

## 6. Checklist final antes de abrir a demanda

- [ ] Template preenchido e anexado (ou linkado) no ticket.
- [ ] SQL esboçada roda (nem que seja parcial) no ambiente de exploração.
- [ ] Campos do catálogo confirmados ou sinalizados como pendentes.
- [ ] Cenário de validação definido com fonte de verdade conhecida.

Assim o time de engenharia consegue transformar rapidamente os requisitos em nodes Orion, mantendo rastreabilidade e garantindo que o “idioma SQL” continue sendo o elo comum entre analistas e engenheiros.
