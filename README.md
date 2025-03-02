# MiniAgent - 轻量级智能代理框架

🌟 **简洁高效的语言模型交互框架**  
专为快速集成大语言模型（LLM）和工具调用设计，轻量化、模块化，适合构建智能对话系统和自动化工作流。

---

## 🚀 核心特性

- **轻量化设计**：代码精简，无冗余依赖，快速部署
- **工具热插拔**：通过装饰器一键定义工具，运行时动态增删
- **多模型兼容**：支持OpenAI及兼容API的大模型（如GLM等）
- **对话管理**：自动维护上下文，支持工具调用中间状态
- **灵活配置**：实时调整温度值、最大token等模型参数

---

## 🛠️ 快速开始

### 基础使用
```python
from MiniAgent.core import ChatOpenAI, Agent, tool

# 定义工具
@tool(description="获取当前时间")
def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")

# 初始化LLM
llm = ChatOpenAI(api_key="YOUR_KEY", model_name="glm-4", base_url="https://your.api")

# 创建Agent
agent = Agent(llm=llm, tools=[get_time])

# 运行对话
response = agent.run("现在几点？")
print(response[-1]['content'])  # 输出：当前时间：2024-03-15 14:30:00
```

---

## 📦 核心组件

### `Agent`
- 管理工具集和对话流程
- 自动协调LLM推理与工具调用
- 支持运行时配置更新

### `ChatOpenAI`
- 兼容主流大模型API
- 支持参数动态调整
- 提供配置保存/加载功能

### `Tool`
```python
@tool  # 用装饰器快速定义工具
def calculate(expression: str):
    """执行数学计算"""
    return eval(expression)
```

### `Conversation`
- 自动维护消息历史
- 支持系统/用户/助手/工具多种角色
- 提供对话上下文序列化

---

## 📚 最佳实践
```python
# 多工具协同示例
agent.set_tools([get_weather, calculate])

response = agent.run("北京气温如何？如果明天下雨，计算15*0.8")
# 1. 调用天气查询
# 2. 执行数学计算
# 3. 综合生成最终回复
```

---

## 💡 设计理念
- **轻如鸿毛**：核心代码<500行，无复杂依赖
- **灵活扩展**：通过继承轻松定制组件
