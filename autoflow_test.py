from MiniAgent.workflow.autoflow import AutoFLow
from MiniAgent.core import Agent,ChatOpenAI,tool
from MiniAgent.tools import duckduckgo_search,fetch_web_content,BochaSearch
import time


def get_time():

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

bocha_search = BochaSearch(api_key='')

if __name__ == '__main__':
    chat_llm = ChatOpenAI()
    chat_llm.load_config("doubao.json")
    chat_llm.set_max_tokens(4096)
    agent = Agent(llm=chat_llm,tools=[bocha_search,fetch_web_content])
    af = AutoFLow(agent=agent)
    af.build_graph(f"现在的时间是{get_time()},请帮我分析小米SU7ultra这辆车的销量以及竞争优势")
    af.run()