from .node import Node
from .edge import Edge

class Graph:

    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, start_node: Node, end_node: Node, edge: Edge):
        # 如果传入为node，则创建edge
        if isinstance(start_node, Node) and isinstance(end_node, Node):
            edge = Edge(start_node, end_node)
            self.edges.append(edge)
        elif isinstance(edge, Edge):
            self.edges.append(edge)

    def remove_node(self, node):
        if node in self.nodes:
            for edge in node.edges:
                self.remove_edge(edge)
            self.nodes.remove(node)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def build(self):
        pass

    def run(self):
        pass