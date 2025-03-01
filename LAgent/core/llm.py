from openai import OpenAI
from typing import Union, List, Dict, Any, Optional
from .message import Message,Conversation

class ChatOpenAI:
    def __init__(
            self,
            api_key: str, 
            base_url: str, 
            model_name: str, 
            stream: bool = False,
            temperature: float = 0.7,
            max_tokens: int  = 1024,
            top_p: float = None,
            frequency_penalty: float = None,
        ):

        self.api_key: str = api_key
        self.base_url: str = base_url
        self.model_name: str = model_name

        self.temperature: float = temperature
        self.max_tokens: int  = max_tokens
        self.top_p: float = top_p
        self.frequency_penalty: float = frequency_penalty

        self.tool_choices = "auto"
        
        self.stream: bool = stream

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)


    def set_stream(self, stream: bool):
        self.stream = stream

    def set_temperature(self, temperature: float):
        self.temperature = temperature

    def set_max_tokens(self, max_tokens: int):
        self.max_tokens = max_tokens

    def set_top_p(self, top_p: float):
        self.top_p = top_p

    def set_frequency_penalty(self, frequency_penalty: float):
        self.frequency_penalty = frequency_penalty

    def set_tool_choices(self, tool_choices: list):
        self.tool_choices = tool_choices

    def generate(
                self, 
                messages: Union[List[Dict[str,Any]], Conversation],
                tools: Optional[list[Dict]] = None) -> Dict[str, Any]:
        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if tools:
            kwargs["tools"] = tools
            # kwargs["tool_choices"] = self.tool_choices

        response = self.client.chat.completions.create(**kwargs)
        print(response.choices[0].message.content)
        return self._format_response(response)

    def _format_response(self, response):
        if hasattr(response, 'choices'):
            message = response.choices[0].message
            message_dict = {
                "content": message.content,
                "role": "assistant",
            }
            
            if hasattr(message, 'tool_calls') and message.tool_calls:
                tool_calls_list = []
                for tool_call in message.tool_calls:
                    tool_calls_list.append({
                        "id": tool_call.id,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        },
                        "type": "function"
                    })
                message_dict["tool_calls"] = tool_calls_list
            
            return {
                "choices": [{
                    "message": message_dict,
                    "index": 0,
                    "finish_reason": "stop"
                }]
            }
        else:
            return response
