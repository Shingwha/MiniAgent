from typing import Dict, List, Any, Optional, Union, Callable
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

    def reset(self):
        self.conversation = Conversation()
        self.tools = []

    def run(self,query: str = None):
        self.conversation.add_system_message(self.system_prompt)
        self.conversation.add_user_message(query)
        while True:
            response = self.llm.generate(messages=self.conversation.get_messages(),
                                        tools=[self.get_tool_instance(tool).to_dict() for tool in self.tools] if self.tools else None )
            message, content, tool_calls = self._parse_llm_response(response)
            if tool_calls:
                self.conversation.add_assistant_message(content)
                tool_results = self._execute_tool_calls(tool_calls)
                for tool_result in tool_results:
                    self.conversation.add_tool_result(tool_result["content"], tool_result["tool_call_id"])
            else:
                self.conversation.add_assistant_message(content)
                break
        return self.conversation.get_messages()

    def _parse_llm_response(self, response):
        message = response["choices"][0]["message"]
        content = message.get("content") or ""  # 处理content为None的情况
        tool_calls = message.get("tool_calls", [])
        
        return message, content, tool_calls

    def _execute_tool_calls(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_call_id = tool_call["id"]
            function = tool_call["function"]
            tool_name = function["name"]
            matching_tool = None
            for tool in self.tools:
                tool_instance = self.get_tool_instance(tool)
                if tool_instance.name == tool_name:
                    matching_tool = tool_instance
                    break
            
            if matching_tool:
                try:
                    import json
                    arguments = json.loads(function.get("arguments", "{}"))
                    result = matching_tool.execute(**arguments)
                    
                    results.append({
                        "tool_call_id": tool_call_id,
                        "content": str(result)
                    })
                except Exception as e:
                    error_message = f"工具执行错误: {str(e)}"
                    results.append({
                        "tool_call_id": tool_call_id,
                        "content": error_message
                    })
            else:
                error_message = f"找不到名为 '{tool_name}' 的工具"
                results.append({
                    "tool_call_id": tool_call_id,
                    "content": error_message
                })
                
        return results
    @staticmethod
    def get_tool_instance(tool_or_func):
        if isinstance(tool_or_func, Tool):
            return tool_or_func
        elif hasattr(tool_or_func, '_tool'):
            return tool_or_func._tool
        else:
            raise TypeError(f"无法从类型 {type(tool_or_func)} 获取Tool实例")