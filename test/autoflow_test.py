from MiniAgent.workflow.autoflow import AutoFLow
from MiniAgent.core import Agent, ChatOpenAI
from MiniAgent.tools import fetch_web_content, BochaSearch


if __name__ == "__main__":
    llm = ChatOpenAI()
    llm.load_config("doubao.json")
    api_key = "s"
    bocha_search = BochaSearch(api_key=api_key)
    agent = Agent(llm=llm, tools=[bocha_search, fetch_web_content])
    af = AutoFLow(agent=agent)
    af.build_graph("查一下有关小米SU7Ultra的信息，然后写一个评测视频的脚本")
    af.run()
