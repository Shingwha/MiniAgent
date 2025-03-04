from .node import Node

class Edge():

    def __init__(self, start_node: Node, end_node: Node):
        self.start_node = start_node
        self.end_node = end_node

    def __repr__(self):
        return f"Edge({self.start_node.name} -> {self.end_node.name})"
