from typing import Callable, List, Any

class Node:
    def __init__(self, func: Callable, inputs: List[str], outputs: List[str], name: str = None):
        self.func = func
        self.inputs = inputs or []
        self.outputs = outputs or []
        self.name = name or func.__name__

    def run(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        # Normalize to tuple/list to map to outputs
        if len(self.outputs) == 0:
            return []
        if len(self.outputs) == 1:
            return [result]
        if isinstance(result, (list, tuple)) and len(result) == len(self.outputs):
            return list(result)
        raise ValueError(f"Node '{self.name}' returned incompatible outputs.")
