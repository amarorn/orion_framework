import pandas as pd

def extract(context):
    df = context.catalog.load("clientes_raw")
    context.logger.info(f"Extract: {len(df)} linhas")
    return df
