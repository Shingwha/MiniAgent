from MiniAgent.core import ChatOpenAI
from typing import Literal


class DeepSeek(ChatOpenAI):
    def __init__(
        self,
        api_key,
        base_url="https://api.deepseek.com/v1",
        model_name: Literal["deepseek-chat", "deepseek-reasoner"] = "deepseek-chat",
        **kwargs,
    ):
        super().__init__(
            api_key=api_key, model_name=model_name, base_url=base_url, **kwargs
        )
