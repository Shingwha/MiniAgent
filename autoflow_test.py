from MiniAgent.workflow.autoflow import AutoFLow
from MiniAgent.core import Agent,ChatOpenAI,tool
from MiniAgent.tools import duckduckgo_search,fetch_web_content,BochaSearch
import time
import os

def get_time():

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

api_key = "your_api_key"
bocha_search = BochaSearch(api_key=api_key)

if __name__ == '__main__':
    chat_llm = ChatOpenAI()
    chat_llm.load_config("doubao.json")
    chat_llm.set_max_tokens(4096)
    api_key = "your_api_key"
    bocha_search = BochaSearch(api_key=api_key)
    agent = Agent(llm=chat_llm,tools=[bocha_search,fetch_web_content])
    af = AutoFLow(agent=agent)
    af.build_graph(f"帮我搜一下有关小米SU7ultra这辆车相关的信息，车的每一项信息都要全面搜索，然后写一个报告给我")
    af.run()