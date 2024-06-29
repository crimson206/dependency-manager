import os
import toml
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List
from crimson.file_loader import filter_paths


def parse_pyproject_toml(directory: str) -> Dict[str, List[str]]:
    dependencies: Dict[str, List[str]] = {}
    for root, dirs, files in os.walk(directory):

        for file in files:
            if file == "pyproject.toml":
                try:
                    path = os.path.join(root, file)
                    with open(path, "r") as f:
                        data = toml.load(f)
                        module_name: str = data["project"]["name"]
                        module_dependencies: List[str] = data["project"].get(
                            "dependencies", []
                        )
                        dependencies[module_name] = module_dependencies
                except Exception:
                    continue
    return dependencies


def build_dependency_graph(dependencies: Dict[str, List[str]]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for module, deps in dependencies.items():
        graph.add_node(module)
        for dep in deps:
            dep_name = dep.split()[0]  # Get the dependency name without version
            graph.add_edge(module, dep_name)
    return graph


def visualize_dependency_graph(graph: nx.DiGraph) -> None:
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12, 8))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        font_size=10,
        font_weight="bold",
        edge_color="gray",
    )
    plt.title("Dependency Map")
    plt.show()
