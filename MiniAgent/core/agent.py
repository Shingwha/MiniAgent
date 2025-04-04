from typing import List, Optional, Union, Callable
import json
from dataclasses import dataclass, field
from .tool import Tool
from .message import Conversation
from .memory import Memory,MemoryBank


@dataclass
class Agent:
    name: Optional[str] = None
    llm: Optional[object] = None
    tools: List[Union[Tool, Callable]] = field(default_factory=list)
    system_prompt: str = "你是一个智能代理，协调LLM和工具使用"
    content_prompt: str = None
    conversation: Conversation = field(default_factory=Conversation)
    memorybank: MemoryBank = field(default_factory=MemoryBank)

    def __post_init__(self):
        if self.name is None:
            self.name = self.__class__.__name__

    def __repr__(self):
        return f"Agent(name={self.name}, llm={self.llm.name}, tools={[tool.name for tool in self.tools]}, system_prompt={self.system_prompt}, content_prompt={self.content_prompt}, conversation={self.conversation})"

    def set_name(self, name: str):
        self.name = name

    def set_llm(self, llm: object):
        self.llm = llm

    def set_tools(self, tools: list):
        self.tools = tools

    def set_system_prompt(self, system_prompt: str):
        self.system_prompt = system_prompt

    def set_content_prompt(self, content_prompt: str):
        self.content_prompt = content_prompt

    def set_memorybank(self, memorybank: MemoryBank):
        self.memorybank = memorybank

    def add_tool(self, tool: Union[Tool, Callable]) -> Optional[str]:
        self.tools.append(tool)

    def add_memory(self, memory: Memory):
        self.memorybank.add_memory(memory)

    def remove_tool(self, tool: Union[Tool, Callable]) -> Optional[str]:
        if tool in self.tools:
            self.tools.remove(tool)

    def remove_memory(self, memory: Memory):
        self.memorybank.remove_memory(memory)

    def clear_conversation(self):
        self.conversation.clear()

    def clear_tools(self):
        self.tools = []

    def clear_memorybank(self):
        self.memorybank.clear()

    def reset(self):
        self.clear_conversation()
        self.clear_tools()

    def copy(self):
        return Agent(llm=self.llm, tools=self.tools, content_prompt=self.content_prompt)

    def run(self, query: str = None):
        if not self.conversation.messages:
            self.conversation.add_system_message(self.system_prompt)
            if self.content_prompt:
                query = self.content_prompt + query
        self.conversation.add_user_message(query)
        while True:
            response = self.llm.generate(
                messages=self.conversation.get_messages(),
                tools=[tool.to_dict() for tool in self.tools] if self.tools else None,
            )
            content = response.content
            tool_calls = response.tool_calls
            if tool_calls:
                self.conversation.add_tool_message(
                    content=content, tool_calls=tool_calls
                )
                tool_results = self._execute_tool_calls(tool_calls)
                for tool_call_id, tool_result in tool_results.items():
                    self.conversation.add_tool_result(
                        content=tool_result, tool_call_id=tool_call_id
                    )
            else:
                self.conversation.add_assistant_message(content)
                break
        print(f"<{self.name}> -> result: {content}")
        return content

    def _execute_tool_calls(self, tool_calls: List[dict]):
        tool_dict = {tool.name: tool for tool in self.tools} if self.tools else {}
        results = {}
        for tool_call in tool_calls:
            try:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                if tool_name in tool_dict:
                    tool = tool_dict[tool_name]
                    result = tool.execute(**arguments)
                    print(
                        f"<{self.name}> -> Executing <{tool_name}> with {arguments} -> Result: {result}"
                    )
                    results[tool_call.id] = str(result)
                else:
                    results[tool_call.id] = f"Tool <{tool_name}> not found: "
            except Exception as e:
                results[tool_call.id] = f"Error executing tool <{tool_name}>: {e}"
        return results
