from ...application.pipeline.builder import PipelineBuilder
from .nodes.extract import extract
from .nodes.transform import transform

def create_pipeline():
    builder = PipelineBuilder("exemplo_get_started")
    
    # Node 1: Extrai dados
    builder.add_node(
        extract,
        inputs=[],  # Não tem inputs
        outputs=["clientes_raw"]  # Produz este output
    )
    
    # Node 2: Transforma dados
    builder.add_node(
        transform,
        inputs=["clientes_raw"],  # Usa o output do node anterior
        outputs=["clientes_processados"]  # Produz este output
    )
    
    return builder.build()

