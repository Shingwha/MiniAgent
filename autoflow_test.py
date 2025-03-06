from MiniAgent.workflow.autoflow import AutoFLow
from MiniAgent.core import Agent,ChatOpenAI
from MiniAgent.workflow.autoflow import AutoFLow

if __name__ == '__main__':
    chat_llm = ChatOpenAI()
    chat_llm.load_config("hunyuan.json")
    agent = Agent(llm=chat_llm)
    
    af = AutoFLow(agent=agent)
    af.build_graph("我需要一份早报，需要包括今明两天的天气，今日AI科技新闻，今日Arxiv论文，根据今天天气信息给我一些提醒和建议，将这些总结后发给我")

    af.graph.run()