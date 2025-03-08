import os
import time
from MiniAgent.core import ChatOpenAI, Agent, tool
from MiniAgent.tools import duckduckgo_search,fetch_web_content,BochaSearch
from MiniAgent.llms import DeepSeek,Doubao


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

# 或者用DeepSeek类
# llm = DeepSeek(api_key="your_api_key")

# 或者用Doubao类
# llm = Doubao(api_key="your_api_key")


agent = Agent(name="general agent",llm=llm, tools=[calculate, get_time])
agent.set_content_prompt(f"你是一个智能助手，当用户问你问题的时候，你需要合理拆解问题，然后分步骤调用工具集来回答用户的问题。用户的问题是：")
# agent.add_tool(duckduckgo_search)  # 添加duckduckgo搜索工具
agent.add_tool(fetch_web_content)  # 添加网页解析工具
agent.add_tool(BochaSearch(api_key="your_api_key"))  # 添加博查搜索工具
while True:
    question = input("请输入你的问题：")
    if question == "exit":
        break
    if question == "clear":
        agent.clear_conversation()
        continue
    agent.run(question)
