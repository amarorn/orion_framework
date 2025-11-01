import pandas as pd

def transform(context, df):
    """Transforma os dados."""
    context.logger.info(f"🔄 Transformando {len(df)} registros")
    
    # Normalizar colunas
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Adicionar categoria de idade
    df["categoria_idade"] = df["idade"].apply(
        lambda x: "jovem" if x < 30 else "adulto"
    )
    
    # Contar por cidade
    por_cidade = df.groupby("cidade").size().to_dict()
    context.logger.info(f"📊 Clientes por cidade: {por_cidade}")
    
    context.logger.info(f"✅ Transformação concluída")
    return df

