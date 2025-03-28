from openai import OpenAI
from typing import Union, List, Dict, Any, Optional
from dataclasses import dataclass
import json
from .message import Conversation


@dataclass
class ChatOpenAI:
    name: str = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_name: Optional[str] = None
    stream: bool = False
    temperature: float = None
    max_tokens: int = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    tool_choices: Optional[list] = None
    client: Optional[OpenAI] = None

    def __post_init__(self):
        if self.name is None:
            self.name = self.__class__.__name__

    def set_api_key(self, api_key: str):
        self.api_key = api_key

    def set_base_url(self, base_url: str):
        self.base_url = base_url

    def set_model_name(self, model_name: str):
        self.model_name = model_name

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

    def load_config(self, file_path: str):
        try:
            with open(file_path, "r") as f:
                config = json.load(f)
                self.api_key = config.get("api_key")
                self.base_url = config.get("base_url")
                self.model_name = config.get("model_name")
        except Exception as e:
            print(f"Error loading config from {file_path}: {e}")

    def save_config(self, file_path: str):
        config = {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "model_name": self.model_name,
        }
        try:
            with open(file_path, "w") as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving config to {file_path}: {e}")

    def generate(
        self,
        messages: Union[List[Dict[str, Any]], Conversation],
        tools: Optional[list[Dict]] = None,
    ) -> Dict[str, Any]:
        kwargs = {
            "model": self.model_name,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
        if self.temperature:
            kwargs["temperature"] = self.temperature
        if self.max_tokens:
            kwargs["max_tokens"] = self.max_tokens

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message  # 直接返回Message对象
