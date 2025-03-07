from MiniAgent.workflow.autoflow import AutoFLow
from MiniAgent.core import Agent,ChatOpenAI,tool


@tool(description="获取天气信息")
def get_weather_info():
    # 这里简单模拟天气信息，实际中可以调用天气 API
    return "今天天气晴朗，气温 20 - 25 摄氏度"

# 模拟获取热点新闻的工具
@tool(description="获取热点新闻")
def get_hot_news():
    # 这里简单模拟热点新闻，实际中可以调用新闻 API
    return "今日热点新闻：雷军主讲汽车发布会，发布小米SU7"

# 模拟生成建议的工具
@tool(description="根据天气信息生成建议")
def generate_suggestions(weather):
    if "晴朗" in weather:
        return "天气晴朗，适合外出活动，记得做好防晒。"
    else:
        return "天气可能多变，出门记得携带雨具。"

@tool(description="生成arxiv论文")
def get_arxiv_papers():
    return "今日AI科技论文相关的有：微软发布AI Agent新架构，使得Agent集群协同工作更高效"



if __name__ == '__main__':
    chat_llm = ChatOpenAI()
    chat_llm.load_config("glm.json")
    chat_llm.set_max_tokens(4096)
    agent = Agent(llm=chat_llm,tools=[get_weather_info, get_hot_news, generate_suggestions, get_arxiv_papers])
    
    af = AutoFLow(agent=agent)
    af.build_graph("我需要一份早报，需要包括今明两天的天气，今日AI科技新闻，今日Arxiv论文，根据今天天气信息给我一些提醒和建议，将这些总结后发给我")
    # af.build_graph("给我一份2024年新能源车企销量的报表")

    af.graph.run()