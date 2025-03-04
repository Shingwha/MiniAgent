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
# 定义计算工具
@tool
def calculate(exp: str):
    return str(eval(exp))

# 切换工具并执行
agent.set_tools([calculate])
print(agent.run("123*456等于多少？"))  # → 56088
```
