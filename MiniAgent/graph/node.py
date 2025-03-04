from typing import Optional
from MiniAgent.core.agent import Agent
import uuid

class Node:

    def __init__(self,name: str, agent: Optional[Agent] = None, is_start: bool = False, is_end: bool = False):
        self.name = name or self.__class__.__name__
        self.agent = agent
        self.in_edges = set()
        self.out_edges = set()
        self.info_from_pre_nodes = []
        self.result = []
        self.is_start = is_start
        self.is_end = is_end

    def run(self):
        if self.agent:
            result = self.agent.run()
        else:
            raise Exception(f"Agent is not set for {self.name}")
        return result


class START(Node):

    self.is_start = True

    def run(self):
        return self.info_from_pre_nodes

class END(Node):
    
    self.is_end = True

    def run(self):
        return self.info_from_pre_nodes
