import importlib
import click
from ...infrastructure.persistence.catalog import DataCatalog
from ...infrastructure.config.context import OrionContext
from ...infrastructure.config.databricks_config import DatabricksConfig, DatabricksConfigError
from ..pipeline.runner import PipelineRunner
from ..viz.export_to_orion_viz import export_pipeline_to_orion_viz

def _load_pipeline(module_path: str, func_name: str):
    mod = importlib.import_module(module_path)
    if not hasattr(mod, func_name):
        raise click.ClickException(f"Função '{func_name}' não encontrada no módulo '{module_path}'.")
    return getattr(mod, func_name)()

@click.group()
def cli():
    '''Oríon CLI'''
    pass

@cli.command()
@click.option("--module", "module_path", required=True, help="Módulo do pipeline (ex: examples.pipeline_clientes.pipeline)")
@click.option("--func", "func_name", default="create_pipeline", show_default=True, help="Factory da pipeline")
@click.option("--catalog", "catalog_path", required=True, help="Caminho para o catalog.yml")
def run(module_path, func_name, catalog_path):
    '''Executa um pipeline.'''
    pipeline = _load_pipeline(module_path, func_name)
    catalog = DataCatalog.from_yaml(catalog_path)
    ctx = OrionContext(catalog=catalog)
    runner = PipelineRunner()
    ctx.logger.info(f"Executando pipeline '{pipeline.name}' ...")
    res = runner.run(pipeline, ctx)
    ctx.logger.info("Pipeline concluída.")
    if res:
        ctx.logger.info(f"Saídas em memória: {list(res.keys())}")

@cli.command()
@click.option("--module", "module_path", required=True, help="Módulo do pipeline")
@click.option("--func", "func_name", default="create_pipeline", show_default=True, help="Factory da pipeline")
@click.option("--output", "output_file", default="orion_viz.json", show_default=True, help="Arquivo JSON de saída")
def viz(module_path, func_name, output_file):
    '''Exporta o grafo da pipeline para JSON.'''
    pipeline = _load_pipeline(module_path, func_name)
    export_pipeline_to_orion_viz(pipeline, output_file)
    click.echo(f"Arquivo gerado: {output_file}")


@cli.command()
@click.option("--config", "config_path", default=None, help="Caminho do arquivo de configuração (padrão: ~/.orion/databricks.yml)")
@click.option("--server-hostname", prompt=True, help="Hostname do workspace Databricks")
@click.option("--http-path", prompt=True, help="HTTP path do SQL warehouse/cluster")
@click.option("--access-token", prompt=True, hide_input=True, help="Token de acesso do Databricks")
@click.option("--catalog", default=None, help="Catalog (opcional)")
@click.option("--schema", default=None, help="Schema (opcional)")
def databricks_config_orion(config_path, server_hostname, http_path, access_token, catalog, schema):
    '''Configura conexão com Databricks de forma centralizada.'''
    try:
        config = DatabricksConfig(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token,
            catalog=catalog,
            schema=schema,
        )
        config.validate()
        config.save(config_path)
        click.echo(f"✅ Configuração do Databricks salva em: {config_path or config.DEFAULT_CONFIG_PATH}")
    except DatabricksConfigError as e:
        raise click.ClickException(str(e))
