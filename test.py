from MiniAgent.core.llm import ChatOpenAI
from MiniAgent.core.agent import Agent
from MiniAgent.core.tool import tool

import os
import time


# 使用装饰器定义工具
@tool
def get_weather(city: str, date: str = "today"):
    """获取指定城市的天气信息
    
    Args:
        city: 城市名称
        date: 日期，默认为今天
    
    Returns:
        天气信息字符串
    """
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
    """计算数学表达式
    
    Args:
        expression: 数学表达式字符串
    
    Returns:
        计算结果
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {str(e)}"

@tool
def get_time():
    """获取当前时间
    
    Returns:
        当前时间字符串
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# OpenAI兼容的API Key和模型名称
# llm = ChatOpenAI(
#     model_name="hunyuan-turbos-20250226",
#     api_key="sk-weyVGyaRPkWjxgROsg27xzFLNIVScfXfNUs9nb3FKcvMxZLz",
#     base_url="https://api.hunyuan.cloud.tencent.com/v1")

llm = ChatOpenAI(
    model_name="glm-4-air-0111",
    api_key="1f4fff3f274d4f8990754cd1ee66e001.Eud0KAAYoLLrLE0h",
    base_url="https://open.bigmodel.cn/api/paas/v4/")

# 创建Agent并添加工具
agent = Agent(llm=llm, tools=[get_weather, get_time])
response = agent.run("今天几号了？现在几点钟了")
print(f"\n最终回答：\n{response[-1]['content']}")


response = agent.run("北京、杭州、上海今天的天气怎么样？")
print(f"\n最终回答：\n{response[-1]['content']}")

# 重置对话历史并切换工具
agent.reset_conversation()
agent.set_tools([calculate])  # 切换到计算工具

response = agent.run("666*9999-1458020")
print(f"\n最终回答：\n{response[-1]['content']}")

agent.reset_conversation()

agent.remove_tool("get_weather")  # 移除天气工具
response = agent.run("北京现在什么天气")
print(f"\n最终回答：\n{response[-1]['content']}")
