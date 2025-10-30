def load(context, df):
    context.catalog.save("clientes_tratado", df)
    context.logger.info("Load: dataset salvo em 'clientes_tratado'")
