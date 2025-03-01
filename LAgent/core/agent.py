from typing import Dict, List, Any, Optional, Union, Callable
from LAgent.core import Tool

class Agent:
    def __init__(
            self,
            name: str = None,
            llm: object = None,
            tools: Optional[List[Union[Tool, Callable]]] = None,
            ):
        
        self.name: str = name
        self.llm: object = llm
        self.tools: list = tools


    def set_name(self, name: str):
        self.name = name

    def set_llm(self, llm: object):
        self.llm = llm

    def set_tools(self, tools: list):
        self.tools = tools

    def add_tool(self, tool: Union[Tool, Callable]) -> Optional[str]:
        self.tools.append(tool)

    def transfer_params_to_llm(self):
        if self.llm is not None:
            self.llm.set_tools(self.tools)
            self.llm.set_question(self.question)

    def run(self,question: str = None):
        self.set_question(question)
        self.transfer_params_to_llm()
        return self.llm.run()
