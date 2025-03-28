from .node import Node


class Edge:
    def __init__(self, start_node: Node, end_node: Node):
        self.start_node = start_node
        self.end_node = end_node
        start_node.out_edges.add(self)
        end_node.in_edges.add(self)

    def __repr__(self):
        return f"Edge({self.start_node.name} -> {self.end_node.name})"
