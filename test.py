from LAgent.core import ChatOpenAI
from LAgent.core import Agent

llm = ChatOpenAI(
                api_key="bde29faa8cf14f1c9b0293b301b26422.Gzf8laK0DwNQnfcj",
                base_url="https://open.bigmodel.cn/api/paas/v4/",
                model_name="glm-4-flash")
# llm.run("写一首诗给我看看")

agent = Agent(llm=llm)
agent.run("写一首诗给我看看")

# agent = Agent(llm=llm)
# agent.set_question("写一首诗给我看看")
# agent.run()