class Node:
    def __init__(
        self, name: str = None, description=None, agent=None, type: str = None
    ):
        self.name = name or self.__class__.__name__
        self.agent = agent
        self.in_edges = set()
        self.out_edges = set()
        self.info_from_pre_nodes = []
        self.result = []
        self.type = type or self.__class__.__name__
        self.description = description

    def set_agent(self, agent):
        self.agent = agent

    def run(self, query):
        if self.agent:
            self.agent.clear_conversation()
            result = self.agent.run(str(query))
        else:
            raise Exception(f"Agent is not set for {self.name}")
        return result


class START(Node):
    def __init__(self):
        super().__init__(description="流程开始")

    def run(self, query):
        return self.info_from_pre_nodes


class END(Node):
    def __init__(self):
        super().__init__(description="流程结束")

    def run(self, query):
        return self.info_from_pre_nodes


if __name__ == "__main__":
    test_node = START()
    print(test_node.type)
    print(test_node.name)
    print(test_node.description)
