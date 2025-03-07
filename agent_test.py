from MiniAgent.core import ChatOpenAI, Agent, tool
from MiniAgent.tools import duckduckgo_search,fetch_web_content
import os
import time



@tool(description="计算具体表达式")
def calculate(expression: str):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {str(e)}"

@tool(description="获取今天日期和现在的具体时间")
def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# OpenAI兼容的API Key和模型名称
llm = ChatOpenAI()
llm.load_config("doubao.json") # 格式为{"api_key":"your_api_key","model_name":"your_model_name","base_url":"your_base_url"}


# 或者直接用下面
# llm = ChatOpenAI(api_key="your_api_key", model_name="your_model_name",base_url="your_base_url")

agent = Agent(name="general agent",llm=llm, tools=[calculate, get_time])
agent.set_content_prompt("你是用户的知心朋友，你的语气需要很自然很友善，略带一些俏皮，下面是用户的问题，请你合理回答：")
agent.add_tool(duckduckgo_search)  # 添加搜索工具
agent.add_tool(fetch_web_content)  # 添加网页解析工具
while True:
    question = input("请输入你的问题：")
    agent.run(question)
