from MiniAgent.core.agent import Agent
from MiniAgent.workflow.graph import Graph
from MiniAgent.workflow.node import Node, START, END
import re
from typing import Dict, List


class AutoFLow:
    def __init__(self, agent: Agent):
        self.graph = Graph()
        self.agent = agent

    # 获取流程代码
    def get_flow_code(self, query: str):
        if query:
            content_prompt = """
            1.你将收到一个问题，请将你这个问题拆成几个明确的子任务
            2.子任务之间需要有联系，每个子任务需要有目标和输入，有些子任务的输入数据是其他子任务的输出数据。
            3.如果用户的问题比较简单，请你适当拓展（比如定义、主要用途、核心功能、技术特点等等）
            现在用户的问题如下：
            """
            agent_for_subtask = self.agent.copy()
            agent_for_subtask.clear_tools()
            agent_for_subtask.set_content_prompt(content_prompt)
            response = agent_for_subtask.run(query)

            content_prompt = """
            1.你将接收到一个需求，请根据需求构建一个xml流程代码
            2.必须严格按照格式要求编写xml流程代码
            3.每个node有name和description属性
            4.必须以START节点开始，以END节点结束
            5.节点在处理输入信息后将结果作为输出信息
            6.节点之间互相独立，只能获取上一个节点的输出信息作为输入依据
            7.description必须明确说明，不能有模糊的描述
            8.格式需要和下方example一样
            9.以```xml开头，以```结尾，不需要其他内容

            example:
            需求：需要一个早报，要包括天气信息、根据天气信息给出的建议、热点新闻
            ```xml
            <flowchart>
                <nodes>
                    <node name="START" description="流程开始" />
                    <node name="get_weather" description="你需要获取天气信息" />
                    <node name="get_news" description="你需要获取今日热点新闻" />
                    <node name="get_suggestion" description="你需要根据天气信息给出建议，天气信息如下：" />
                    <node name="generate_report" description="你需要总结天气、建议和新闻生成早报，你将收到一些杂乱的信息，但请你自己整理信息并且给出逻辑清晰的早报，内容要尽可能全面，你获得的信息如下：" />
                    <node name="END" description="流程结束" />
                </nodes>
                <edges>
                    <edge start="START" end="get_weather" />
                    <edge start="START" end="get_news" />
                    <edge start="get_weather" end="get_suggestion" />
                    <edge start="get_news" end="generate_report" />
                    <edge start="get_suggestion" end="generate_report" />
                    <edge start="get_weather" end="generate_report" />
                    <edge start="generate_report" end="END" />
                </edges>
            </flowchart>
            ```
            现在请你根据要求和用户的需求，构建xml流程代码，并将代码发送给我。
            用户的需求是：
            """
            agent_for_xml = self.agent.copy()
            agent_for_xml.set_content_prompt(content_prompt)
            response = agent_for_xml.run(response)
            return response
        else:
            print("请输入需求")

    def add_to_graph(self, nodes: Dict, edges: List):
        node_objs = {}

        for node_id, data in nodes.items():
            if node_id == "START":
                node = START()
            elif node_id == "END":
                node = END()
            else:
                node = Node(name=data["name"], description=data["description"])
                node.type = "process"
            node_objs[node_id] = node
            self.graph.add_node(node)

        # 创建边对象
        for start_id, end_id in edges:
            start_node = node_objs.get(start_id)
            end_node = node_objs.get(end_id)
            if start_node and end_node:
                self.graph.add_edge(start_node, end_node)

    def parse_flow_code(self, xml_str: str) -> Dict:
        nodes = {}
        edges = []
        node_matches = re.findall(
            r'<node name="(.*?)" description="(.*?)" */?>', xml_str
        )
        for name, description in node_matches:
            nodes[name] = {"name": name, "description": description}
        edge_matches = re.findall(r'<edge start="(.*?)" end="(.*?)" */?>', xml_str)
        for start, end in edge_matches:
            edges.append((start, end))

        return nodes, edges

    def build_graph(self, query: str):
        if query:
            flow_code = self.get_flow_code(query)
            nodes, edges = self.parse_flow_code(flow_code)
            self.add_to_graph(nodes, edges)
            self.set_nodes_agent(self.agent)
            return self.graph

    def set_nodes_agent(self, agent: Agent):
        for node in self.graph.nodes:
            if node.type == "START" or node.type == "END":
                continue
            else:
                agent_copy = agent.copy()
                node.set_agent(agent_copy)
                node.agent.set_content_prompt(node.description)

    def run(self, query: str = ""):
        self.graph.run(query)
