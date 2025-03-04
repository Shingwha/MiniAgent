from .node import Node
from .edge import Edge

class Graph:

    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node) -> None:
        self.nodes.append(node)

    def add_edge(self, start_node: Node, end_node: Node) -> None:
        self.edges.append(Edge(start_node, end_node))

    def remove_node(self, node: Node) -> None:
        if node in self.nodes:
            for edge in node.edges:
                self.remove_edge(edge)
            self.nodes.remove(node)

    def remove_edge(self, start_node: Node, end_node: Node) -> None:
        for edge in self.edges:
            if edge.start_node == start_node and edge.end_node == end_node:
                self.edges.remove(edge)
                break

    def build(self):
        pass

    def run(self):
        pass
