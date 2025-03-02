from typing import Dict, List, Any, Optional, Union, Callable
import json
from .tool import Tool
from .message import Conversation

class Agent:
    def __init__(
            self,
            name: str = None,
            llm: object = None,
            tools: Optional[List[Union[Tool, Callable]]] = None,
            ):
        
        self.name = name
        self.llm = llm
        self.tools = tools
        self.system_prompt = "你是一个智能代理，协调LLM和工具使用"
        self.conversation = Conversation()

    def set_name(self, name: str):
        self.name = name

    def set_llm(self, llm: object):
        self.llm = llm

    def set_tools(self, tools: list):
        self.tools = tools

    def add_tool(self, tool: Union[Tool, Callable]) -> Optional[str]:
        self.tools.append(tool)

    def remove_tool(self, tool: Union[Tool, Callable]) -> Optional[str]:
        if tool in self.tools:
            self.tools.remove(tool)

    def reset_conversation(self):
        self.conversation = Conversation()

    def reset_tools(self):
        self.tools = []

    def reset(self):
        self.reset_conversation()
        self.reset_tools()

    def run(self,query: str = None):
        if self.conversation.messages == []:
            self.conversation.add_system_message(self.system_prompt)
        self.conversation.add_user_message(query)
        while True:
            response = self.llm.generate(messages=self.conversation.get_messages(),
                                        tools=[self.get_tool_instance(tool).to_dict() for tool in self.tools] if self.tools else None )
            content = response.content
            tool_calls = response.tool_calls
            if tool_calls:
                self.conversation.add_tool_message(content=content, tool_calls=tool_calls)
                for tool_call in tool_calls:
                    tool_result = self._execute_tool_call(tool_call)
                    self.conversation.add_tool_result(content=tool_result,tool_call_id=tool_call.id)
            else:
                self.conversation.add_assistant_message(content)
                break
        return self.conversation.get_messages()


    def _execute_tool_call(self, tool_call: dict):
        try:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            # 查找匹配工具
            for tool in self.tools:
                tool_instance = self.get_tool_instance(tool)
                if tool_instance.name == tool_name:
                    result = tool_instance.execute(**arguments)
                    print(f"\nExecuting tool <{tool_name}> with arguments {arguments} -> Result: {result}")
                    return str(result)
            return f"Tool <{tool_name}> not found"
        except Exception as e:
            return f"Tool error: {str(e)}"

    @staticmethod
    def get_tool_instance(tool_or_func):
        if isinstance(tool_or_func, Tool):
            return tool_or_func
        elif hasattr(tool_or_func, '_tool'):
            return tool_or_func._tool
        else:
            raise TypeError(f"无法从类型 {type(tool_or_func)} 获取Tool实例")