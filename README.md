# MiniAgent - 小型智能代理框架

轻量级Agent框架，用于快速构建基于LLM的智能代理系统，支持工具扩展与任务编排。

## 核心特性

- **模块化设计**：Agent/Node/Edge/Tool 解耦
- **工具集成**：通过装饰器快速定义工具函数
- **对话管理**：完整的会话历史追踪机制
- **工作流编排**：支持构建节点关系图（Graph）

```python
from MiniAgent.core import Agent, ChatOpenAI, tool

@tool(description="获取天气")
def get_weather(city: str):
    return f"{city}天气晴朗"

llm = ChatOpenAI(api_key="your_key", model_name="deepseek-v3", base_url="https://api.deepseek.com/v1")
agent = Agent(llm=llm, tools=[get_weather])
print(agent.run("北京天气如何？"))
```
<div style="text-align: center;">
<img src="https://github.com/user-attachments/assets/7b9d5536-38ca-496b-a65e-60ee927154a0" width="50%" alt="image">
</div>

## 核心模块

| 模块       | 说明                          |
|------------|-----------------------------|
| `Agent`    | 代理核心，协调LLM与工具调用       |
| `Node`     | 工作流节点，可绑定Agent          |
| `Graph`    | 节点关系图，支持流程编排           |
| `tool`     | 工具装饰器，快速扩展代理能力        |
| `Message`  | 对话消息结构，支持工具调用追踪       |

## 示例场景


```python
from MiniAgent.core import Agent, ChatOpenAI, tool
from MiniAgent.workflow import Graph, Node, START, END

# 模拟获取天气信息的工具
@tool
def get_weather_info():
    # 这里简单模拟天气信息，实际中可以调用天气 API
    return "今天天气晴朗，气温 20 - 25 摄氏度"

# 模拟获取热点新闻的工具
@tool
def get_hot_news():
    # 这里简单模拟热点新闻，实际中可以调用新闻 API
    return "今日热点新闻：科技公司发布新的智能产品，引发市场关注。"

# 模拟生成建议的工具
@tool
def generate_suggestions(weather):
    if "晴朗" in weather:
        return "天气晴朗，适合外出活动，记得做好防晒。"
    else:
        return "天气可能多变，出门记得携带雨具。"

# 初始化大语言模型
llm = ChatOpenAI()
llm.load_config("hunyuan.json")

# 创建 Agent
agent = Agent(llm=llm)

# 创建节点
start_node = START()
get_weather_node = Node(name="get_weather", agent=agent, tool=get_weather_info)
get_news_node = Node(name="get_news", agent=agent, tool=get_hot_news)
generate_suggestions_node = Node(name="generate_suggestions", agent=agent, tool=generate_suggestions)
generate_newsletter_node = Node(name="generate_newsletter", agent=agent)
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
result = workflow.run("生成早报")
print(result)

```
![image](https://github.com/user-attachments/assets/dd8e32ac-6286-4947-b39a-a345a9ff69d0)
