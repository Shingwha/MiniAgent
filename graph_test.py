from MiniAgent.core import Agent,ChatOpenAI,tool
from MiniAgent.workflow import Graph,Node,START,END

llm_1 = ChatOpenAI()
llm_1.load_config("hunyuan.json")

llm_2 = ChatOpenAI()
llm_2.load_config("hunyuan.json")

agent_1 = Agent(llm = llm_1)
agent_2 = Agent(llm = llm_2,system_prompt="你是一个文学专家，能将得到的信息用一句话概述")

test_node_1 = Node(name="test_node_1",agent=agent_1)
test_node_2 = Node(name="test_node_2",agent=agent_2)

workflow = Graph(name="workflow_test")
workflow.add_node(test_node_1)
workflow.add_node(test_node_2)

workflow.add_edge(test_node_1,test_node_2)

result = workflow.run("给我讲一个幽默的故事，要发生在学校") 

