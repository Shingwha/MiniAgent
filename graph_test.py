from MiniAgent.core import Agent, ChatOpenAI, tool
from MiniAgent.workflow import Graph, Node, START, END


# 模拟获取天气信息的工具
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

# 初始化大语言模型
llm = ChatOpenAI()
llm.load_config("hunyuan.json")
# llm.load_config("glm.json")

# 创建 Agent
get_weather_agent = Agent(llm=llm,tools=[get_weather_info],content_prompt="你需要调用工具获取天气")
get_news_agent = Agent(llm=llm,tools=[get_hot_news],content_prompt="你需要调用工具获取热点新闻")
generate_suggestions_agent = Agent(llm=llm,tools=[generate_suggestions],content_prompt="当你接收到天气信息的时候，你需要给出对应的建议：")
generate_newsletter_agent = Agent(llm=llm,content_prompt="你将会接收到不同类别的信息，你需要对它们进行整合，生成一个早起人专属的早报,可以加一些可爱的表情😊：")
# 创建节点
start_node = START()
get_weather_node = Node(name="get_weather", agent=get_weather_agent)
get_news_node = Node(name="get_news", agent=get_news_agent)
generate_suggestions_node = Node(name="generate_suggestions", agent=generate_suggestions_agent)
generate_newsletter_node = Node(name="generate_newsletter", agent=generate_newsletter_agent)
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
