from openai import OpenAI
from LAgent.core.message import Message

class ChatOpenAI:
    def __init__(
            self,
            api_key: str, 
            base_url: str, 
            model_name: str, 
            stream: bool = False,
            temperature: float = None,
            max_tokens: int  = None,
            top_p: float = None,
            frequency_penalty: float = None,
            tools: list = None,
            tool_choices: list = None
        ):

        self.api_key: str = api_key
        self.base_url: str = base_url
        self.model_name: str = model_name

        self.temperature: float = temperature
        self.max_tokens: int  = max_tokens
        self.top_p: float = top_p
        self.frequency_penalty: float = frequency_penalty

        self.tools: list = tools
        self.tool_choices: list = tool_choices
        
        self.stream: bool = stream
        self.system_prompt: str = """You are a helpful assistant."""
        self.messages: list = None

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def set_question(self, question: str):
        self.question = question

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

    def set_tools(self, tools: list):
        self.tools = tools

    def set_tool_choices(self, tool_choices: list):
        self.tool_choices = tool_choices

    def add_message(self, message: Message):
        self.messages.append(message)


    def run(self, question: str = None):
        if question is not None:
            self.set_question(question)
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.question},
                    ],
            stream=self.stream,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            tools=self.tools
        )
        print(response.choices[0].message.content)
        return response
