from typing import List
from ...core.entities.node import Node
from ...core.entities.pipeline import Pipeline

class PipelineBuilder:
    def __init__(self, name: str):
        self.name = name
        self._nodes: List[Node] = []

    def add_node(self, func, inputs=None, outputs=None, name: str = None):
        self._nodes.append(Node(func=func, inputs=inputs or [], outputs=outputs or [], name=name))
        return self

    def build(self) -> Pipeline:
        return Pipeline(self.name, self._nodes)
