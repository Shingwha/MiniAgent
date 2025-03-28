from MiniAgent.core import ChatOpenAI
from typing import Literal


class Doubao(ChatOpenAI):
    def __init__(
        self,
        api_key,
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        model_name: Literal[
            "doubao-1-5-lite-32k-250115", "doubao-1-5-pro-32k-250115"
        ] = "doubao-1-5-lite-32k-250115",
        **kwargs,
    ):
        super().__init__(
            api_key=api_key, model_name=model_name, base_url=base_url, **kwargs
        )
