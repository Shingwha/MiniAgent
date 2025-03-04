from MiniAgent.core import ChatOpenAI, Agent, tool

import os
import time


# 使用装饰器定义工具
@tool(description="获取指定城市的天气信息")
def get_weather(city: str, date: str = "today"):
    # 这里应该是实际的天气API调用
    if city == "北京":
        return f"{city}在{date}的天气晴朗，温度25°C"
    elif city == "杭州":
        return f"{city}在{date}的天气多云，温度20°C"
    elif city == "上海":
        return f"{city}在{date}的天气阴，温度22°C"
    return f"{city}在{date}的天气晴朗，温度25°C"

@tool
def calculate(expression: str):
    """
    计算数学表达式
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {str(e)}"

@tool
def get_time():
    """
    获取当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())




# OpenAI兼容的API Key和模型名称
llm = ChatOpenAI()
llm.load_config("glm.json")

# 或者直接用下面
# llm = ChatOpenAI(api_key="your_api_key", model_name="your_model_name",base_url="your_base_url")

agent = Agent(llm=llm, tools=[get_weather, get_time])

response = agent.run("今天几号了？现在几点钟了")
print(f"\n最终回答 -> {response}")


response = agent.run("北京、杭州、上海今天的天气怎么样？")
print(f"\n最终回答 -> {response}")

agent.clear_conversation()
agent.set_tools([calculate])  # 切换到计算工具

response = agent.run("666*9999-1458020")
print(f"\n最终回答 -> {response}")

agent.clear_conversation()

agent.remove_tool("get_weather")  # 移除天气工具后的回复
response = agent.run("北京现在什么天气")
print(f"\n最终回答 -> {response}")
