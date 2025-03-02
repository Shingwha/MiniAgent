
# Agent Framework

一个基于LLM的智能代理框架，支持工具扩展和对话管理，轻松构建AI应用。

## 功能特性

- 🤖 **智能代理**：协调LLM与工具调用，支持多轮对话
- 🧰 **工具扩展**：通过装饰器快速创建工具，支持函数自动参数解析
- 💬 **对话管理**：完整记录系统/用户/助手/工具消息，支持对话重置
- 🔌 **OpenAI集成**：内置ChatOpenAI客户端，支持模型参数配置

## 安装

```bash
pip install openai  # 基础依赖
# 将本框架代码放入项目目录即可使用
```


## 快速开始

### 基本使用示例
```python
from MiniAgent.core import ChatOpenAI, Agent, tool

# 初始化LLM
llm = ChatOpenAI(api_key="your-api-key", model_name="gpt-3.5-turbo")

# 创建工具
@tool()
"""
计算两个数的和
"""
def add(a: int, b: int):
    return a + b

# 创建代理
agent = Agent(llm=llm, tools=[add])

# 运行查询
response = agent.run("请计算12加5等于多少？")
print(response)
```

### 自定义工具示例
```python
@tool(description="获取指定城市的天气")
def get_weather(city: str):
    # 这里实现实际的天气API调用
    return f"{city} 晴，25℃"

agent = Agent(llm=llm, tools=[get_weather])
agent.run("上海现在天气怎么样？")
```

## 核心模块说明

### 🧩 Agent 类
- `run()`: 执行对话流程，自动处理工具调用
- 支持动态添加/移除工具
- 维护对话历史上下文

### 🔧 Tool 系统
- 使用`@tool`装饰器快速创建工具
- 自动生成工具参数schema
- 支持类工具（继承`Tool`类）和函数工具

### 🌐 ChatOpenAI
- 支持OpenAI API完整参数配置
- 提供配置保存/加载功能
- 支持工具调用参数自动传递

### 📩 消息系统
- `Message`类：标准化消息格式
- `Conversation`类：管理对话历史
- 支持工具调用消息和结果记录

## 配置指南

1. 设置API密钥：
```python
llm = ChatOpenAI(api_key="sk-...")
# 或通过配置文件
llm.load_config("config.json")
```

2. 模型参数设置：
```python
llm.set_temperature(0.5)
llm.set_max_tokens(512)
```

## 进阶功能

### 自定义系统提示
```python
agent = Agent()
agent.set_system_prompt("你是一个智能助手，请根据用户的问题，选择合适的工具来回答用户的问题。")
```

### 查看对话历史
```python
for msg in agent.conversation.messages:
    print(f"[{msg.role}] {msg.content}")
```

## 许可证
MIT License
```

> 注意：实际使用时需要替换OpenAI API密钥，并确保网络可以访问OpenAI服务。建议将敏感配置（如API密钥）存储在环境变量或配置文件中。
