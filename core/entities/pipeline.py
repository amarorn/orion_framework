from typing import List, Dict, Any
from .node import Node

class Pipeline:
    def __init__(self, name: str, nodes: List[Node]):
        self.name = name
        self.nodes = nodes

    def run(self, context) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        for node in self.nodes:
            # Prepare inputs: prefer in-memory, fallback to catalog
            inputs = []
            for in_name in node.inputs:
                if in_name in data:
                    inputs.append(data[in_name])
                else:
                    # try load from catalog
                    try:
                        inputs.append(context.catalog.load(in_name))
                    except Exception:
                        raise KeyError(f"Input '{in_name}' not found in memory or catalog for node '{node.name}'.")
            # Execute
            outputs = node.run(context, *inputs)
            # Persist outputs in memory and auto-save if in catalog
            for out_name, value in zip(node.outputs, outputs):
                data[out_name] = value
                if context.catalog.exists(out_name):
                    context.catalog.save(out_name, value)
        return data
