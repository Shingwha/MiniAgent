from .node import Node
from .edge import Edge
from collections import deque

class Graph:

    def __init__(self, name: str = None):
        self.nodes = set()
        self.edges = set()
        self.is_built = False
        self.sorted_nodes = []
        self.name = name or self.__class__.__name__

    def add_node(self, node) -> None:
        self.nodes.add(node)
        self.is_built = False

    def add_edge(self, start_node: Node, end_node: Node) -> None:
        self.edges.add(Edge(start_node, end_node))
        self.is_built = False

    def remove_node(self, node):
        if node in self.nodes:
            for edge in node.in_edges.union(node.out_edges):
                self.remove_edge(edge)
            self.nodes.remove(node)
            self.is_built = False

    def remove_edge(self, edge):
        if edge in self.edges:
            edge.start_node.out_edges.remove(edge)
            edge.end_node.in_edges.remove(edge)
            self.edges.remove(edge)
            self.is_built = False

    def build(self) -> None:
        in_degree = {node: len(node.in_edges) for node in self.nodes}
        queue = deque([node for node, degree in in_degree.items() if degree == 0])
        sorted_nodes = []
        
        while queue:
            node = queue.popleft()
            sorted_nodes.append(node)
            for edge in node.out_edges:
                next_node = edge.end_node
                in_degree[next_node] -= 1
                if in_degree[next_node] == 0:
                    queue.append(next_node)
        
        if len(sorted_nodes) != len(self.nodes):
            raise Exception("Graph build failed: cycle detected")
        self.is_built = True
        self.sorted_nodes = sorted_nodes
        print(f"<{self.name}>:built successfully")

    def run(self,query):
        if self.is_built:
            pass
        else:
            self.build()
        print(f"<{self.name}>:running")
        self.sorted_nodes[0].info_from_pre_nodes = query
        for node in self.sorted_nodes:
            result = node.run(node.info_from_pre_nodes)
            print(f"<{node.name}>:{result}")
            node.result = result
            for edge in node.out_edges:
                edge.end_node.info_from_pre_nodes.append(str(result))
        return self.sorted_nodes[-1].result


            
        
