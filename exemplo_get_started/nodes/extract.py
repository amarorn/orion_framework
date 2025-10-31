import pandas as pd

def extract(context):
    """Extrai dados do catalog."""
    df = context.catalog.load("clientes_raw")
    context.logger.info(f"✅ Extraídos {len(df)} registros de clientes")
    return df

