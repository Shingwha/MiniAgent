from MiniAgent.core import Agent, ChatOpenAI, tool
from MiniAgent.workflow import Graph, Node, START, END
from MiniAgent.tools import BochaSearch
import time


@tool
def get_time():
    """
    获取当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 初始化大语言模型
llm = ChatOpenAI()
llm.load_config("doubao.json")

bocha_search = BochaSearch(api_key="")

# 创建 Agent
get_weather_agent = Agent(
    llm=llm, tools=[bocha_search], content_prompt="你需要调用工具获取长春的天气"
)
get_news_agent = Agent(
    llm=llm,
    tools=[bocha_search, get_time],
    content_prompt="你需要根据今天的日期时间获取当日AI科技新闻",
)
generate_suggestions_agent = Agent(
    llm=llm,
    content_prompt="你将接收到一些天气信息，你需要整合天气信息，并且输出对应的建议：",
)
generate_newsletter_agent = Agent(
    llm=llm,
    content_prompt="你将会接收到不同类别的信息，你需要对它们进行整合，生成一个早起人专属的早报,可以加一些可爱的表情😊：",
)
# 创建节点
start_node = START()
get_weather_node = Node(name="get_weather", agent=get_weather_agent)
get_news_node = Node(name="get_news", agent=get_news_agent)
generate_suggestions_node = Node(
    name="generate_suggestions", agent=generate_suggestions_agent
)
generate_newsletter_node = Node(
    name="generate_newsletter", agent=generate_newsletter_agent
)
end_node = END()

# 创建图
workflow = Graph()

# 添加节点到图
workflow.add_node(start_node)
workflow.add_node(get_weather_node)
workflow.add_node(get_news_node)
workflow.add_node(generate_suggestions_node)
workflow.add_node(generate_newsletter_node)
workflow.add_node(end_node)

# 添加边来定义节点之间的依赖关系
workflow.add_edge(start_node, get_weather_node)
workflow.add_edge(start_node, get_news_node)
workflow.add_edge(get_weather_node, generate_suggestions_node)
workflow.add_edge(get_weather_node, generate_newsletter_node)
workflow.add_edge(get_news_node, generate_newsletter_node)
workflow.add_edge(generate_suggestions_node, generate_newsletter_node)
workflow.add_edge(generate_newsletter_node, end_node)

# 运行工作流
workflow.run()
