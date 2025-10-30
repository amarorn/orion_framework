import json

def export_pipeline_to_orion_viz(pipeline, output_file="orion_viz.json"):
    nodes = []
    edges = []

    for node in pipeline.nodes:
        nodes.append({
            "id": node.name,
            "name": node.name,
            "inputs": node.inputs,
            "outputs": node.outputs,
            "type": "function"
        })
        for inp in node.inputs:
            edges.append({"source": inp, "target": node.name})
        for out in node.outputs:
            edges.append({"source": node.name, "target": out})

    graph = {"nodes": nodes, "edges": edges, "pipeline": pipeline.name}
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)
    return output_file
