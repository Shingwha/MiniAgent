from .node import Node
from .edge import Edge

class Graph:

    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_node(self, node) -> None:
        self.nodes.add(node)

    def add_edge(self, start_node: Node, end_node: Node) -> None:
        self.edges.add(Edge(start_node, end_node))

    def remove_node(self, node):
        if node in self.nodes:
            for edge in node.in_edges.union(node.out_edges):
                self.remove_edge(edge)
            self.nodes.remove(node)

    def remove_edge(self, edge):
        if edge in self.edges:
            edge.start_node.out_edges.remove(edge)
            edge.end_node.in_edges.remove(edge)
            self.edges.remove(edge)

    def build(self):
        pass

    def run(self):
        pass
