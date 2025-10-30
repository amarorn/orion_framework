def transform(context, df):
    # Exemplo simples: normaliza colunas e filtra registros
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.dropna(subset=["nome"])
    context.logger.info(f"Transform: {len(df)} linhas após limpeza")
    return df
