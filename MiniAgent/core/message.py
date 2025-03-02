from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class Message:
    
    role: str
    content: str
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"role": self.role, "content": self.content}
        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id
        if self.tool_calls:
            result["tool_calls"] = self.tool_calls
        return result
        
class Conversation:

    def __init__(self):
        self.messages: List[Message] = []

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    def add_system_message(self, content: str) -> None:
        self.add_message(Message(role="system", content=content))

    def add_user_message(self, content: str) -> None:
        self.add_message(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        self.add_message(Message(role="assistant", content=content))

    def add_tool_message(self, content: str, tool_calls: List[Dict[str, Any]]) -> None:
        self.add_message(Message(role="assistant", content=content, tool_calls=tool_calls))

    def add_tool_result(self, content: str, tool_call_id: str) -> None:
        self.add_message(Message(role="tool", content=content, tool_call_id=tool_call_id))

    def get_messages(self) -> List[Dict[str, Any]]:
        return [message.to_dict() for message in self.messages]

    def clear(self) -> None:
        self.messages = []