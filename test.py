from LAgent.core.llm import ChatOpenAI
from LAgent.core.agent import Agent
from LAgent.core.tool import tool

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
    return f"{city}在{date}的天气晴朗，温度25°C"

# 也可以自定义名称和描述
@tool()
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


# 创建LLM实例
llm = ChatOpenAI(
    model_name="hunyuan-turbos-20250226",
    api_key="sk-weyVGyaRPkWjxgROsg27xzFLNIVScfXfNUs9nb3FKcvMxZLz",
    base_url="https://api.hunyuan.cloud.tencent.com/v1")

# llm = LLM(
#     model_name="glm-4-air-0111",
#     api_key="1f4fff3f274d4f8990754cd1ee66e001.Eud0KAAYoLLrLE0h",
#     base_url="https://open.bigmodel.cn/api/paas/v4/")

# 创建Agent并添加工具
agent = Agent(llm=llm, tools=[get_weather])

# 运行Agent
# start_time = time.time()
# response = agent.run("北京、杭州、上海今天的天气怎么样？")
# end_time = time.time()
# print(f"执行时间: {end_time - start_time:.2f}秒")

# 重置对话历史并切换工具
agent.reset()
agent.set_tools([calculate])  # 切换到计算工具

start_time = time.time()
response = agent.run("计算一下18/3*4-2")
end_time = time.time()
print(f"执行时间: {end_time - start_time:.2f}秒")
