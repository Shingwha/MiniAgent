from typing import Optional
from MiniAgent.core.agent import Agent
import uuid

class Node:

    def __init__(self,name: str, agent: Optional[Agent] = None):
        self.name = name or self.__class__.__name__
        self.agent = agent
        self.edges = []

    def run(self):
        if self.agent:
            result = self.agent.run()
        else:
            raise Exception(f"Agent is not set for {self.name}")
        return result
