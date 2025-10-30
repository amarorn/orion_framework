from ...application.pipeline.builder import PipelineBuilder
from .nodes.extract_clientes import extract
from .nodes.transform_clientes import transform
from .nodes.load_clientes import load

def create_pipeline():
    builder = PipelineBuilder("ingestao_clientes")
    builder.add_node(extract, inputs=[], outputs=["clientes_raw"])
    builder.add_node(transform, inputs=["clientes_raw"], outputs=["clientes_tratado"])
    builder.add_node(load, inputs=["clientes_tratado"], outputs=[])
    return builder.build()
