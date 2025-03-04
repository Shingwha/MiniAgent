from MiniAgent.core import Agent,ChatOpenAI,tool
from MiniAgent.workflow import Graph,Node,START,END

llm_1 = ChatOpenAI()
llm_1.load_config("hunyuan.json")

llm_2 = ChatOpenAI()
llm_2.load_config("hunyuan.json")

agent_1 = Agent(llm = llm_1)
agent_2 = Agent(llm = llm_2)

start_node = START()
test_node_1 = Node(name="test_node_1",agent=agent_1)
test_node_2 = Node(name="test_node_2",agent=agent_2)
end_node = END()

workflow = Graph()
workflow.add_node(start_node)
workflow.add_node(test_node_1)
workflow.add_node(test_node_2)
workflow.add_node(end_node)

workflow.add_edge(start_node,test_node_1)
workflow.add_edge(test_node_1,test_node_2)
workflow.add_edge(test_node_2,end_node)

result = workflow.run("长江黄河哪个更长")

print(str(result))
