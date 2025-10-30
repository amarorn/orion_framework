# Configuração do Databricks no Orion Framework

Este guia mostra como configurar e usar o Databricks de forma centralizada no Orion Framework.

## 1. Configurar Credenciais

Configure suas credenciais do Databricks uma única vez usando o comando CLI:

```bash
orion databricks-config-orion
```

O comando irá solicitar:
- **server-hostname**: Hostname do seu workspace (ex: `workspace.cloud.databricks.com`)
- **http-path**: HTTP path do SQL warehouse (ex: `/sql/1.0/warehouses/abc123def456`)
- **access-token**: Seu token de acesso pessoal do Databricks
- **catalog** (opcional): Catalog padrão
- **schema** (opcional): Schema padrão

A configuração será salva em `~/.orion/databricks.yml`.

### Alternativa: Configuração via Variáveis de Ambiente

Você também pode configurar via variáveis de ambiente:

```bash
export DATABRICKS_SERVER_HOSTNAME="workspace.cloud.databricks.com"
export DATABRICKS_HTTP_PATH="/sql/1.0/warehouses/abc123def456"
export DATABRICKS_ACCESS_TOKEN="dapi..."
export DATABRICKS_CATALOG="hive_metastore"
export DATABRICKS_SCHEMA="default"
```

## 2. Usar no Catalog.yml

Depois de configurar as credenciais, você pode usar datasources do Databricks no seu `catalog.yml`:

```yaml
# Carregar de uma tabela
clientes_raw:
  type: databricks
  table: clientes

# Carregar com query customizada
clientes_ativos:
  type: databricks
  query: "SELECT * FROM clientes WHERE status = 'ativo'"

# Salvar em tabela do Databricks
clientes_processados:
  type: databricks
  table: clientes_processados
  mode: overwrite  # ou 'append'
```

### Opções Avançadas

Você pode sobrescrever catalog e schema por datasource:

```yaml
clientes_analytics:
  type: databricks
  table: clientes
  catalog: analytics_catalog  # Sobrescreve o catalog da config global
  schema: curated              # Sobrescreve o schema da config global
```

## 3. Usar nos Nodes

Use normalmente através do `context.catalog`:

```python
def extract(context: OrionContext):
    # Carrega automaticamente do Databricks
    df = context.catalog.load("clientes_raw")
    context.logger.info(f"Carregados {len(df)} registros")
    return df

def load(context: OrionContext, df):
    # Salva automaticamente no Databricks
    context.catalog.save("clientes_processados", df)
    context.logger.info(f"Salvos {len(df)} registros")
```

## 4. Exemplo Completo

### catalog.yml

```yaml
# Input do Databricks
clientes_raw:
  type: databricks
  table: raw.clientes

# Output para Databricks
clientes_processados:
  type: databricks
  table: analytics.clientes_processed
  mode: overwrite
```

### pipeline.py

```python
from ...infrastructure.config.context import OrionContext

def extract(context: OrionContext):
    df = context.catalog.load("clientes_raw")
    context.logger.info(f"Extraídos {len(df)} registros do Databricks")
    return df

def transform(context: OrionContext, df):
    df = df[df["status"] == "ativo"]
    context.logger.info(f"Transformados: {len(df)} registros")
    return df

def load(context: OrionContext, df):
    context.catalog.save("clientes_processados", df)
    context.logger.info(f"Salvos {len(df)} registros no Databricks")
```

### Executar

```bash
orion run \
  --module examples.pipeline_clientes.pipeline \
  --catalog examples/catalog.yml
```

## Segurança

⚠️ **Importante**: O arquivo `~/.orion/databricks.yml` contém credenciais sensíveis. 

- Não commite este arquivo no git
- Adicione `~/.orion/` ao `.gitignore`
- Use permissões restritas: `chmod 600 ~/.orion/databricks.yml`

## Troubleshooting

### Erro: "Configuração do Databricks não encontrada"

Certifique-se de:
1. Executar `orion databricks-config-orion` primeiro, OU
2. Configurar as variáveis de ambiente necessárias

### Erro: "Falha ao conectar com Databricks"

Verifique:
- Se o `server_hostname` está correto
- Se o `http_path` corresponde a um SQL warehouse ativo
- Se o `access_token` é válido e não expirou

### Verificar Configuração

Para verificar sua configuração, você pode ler o arquivo (cuidado com o token):

```bash
cat ~/.orion/databricks.yml
```

