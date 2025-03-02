from typing import Any, Callable, Dict, List, Optional
import inspect
import functools

class Tool:
    
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = self._get_parameters()

    def _get_parameters(self) -> Dict:
        signature = inspect.signature(self.func)
        parameters = {}
        for param_name, param in signature.parameters.items():
            param_info = {
                "type": "string",
                "description": f"{param_name} 参数"
            }
            parameters[param_name] = param_info
        return parameters

    def execute(self, **kwargs) -> Any:
        result = self.func(**kwargs)
        return result

    def to_dict(self) -> Dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": list(self.parameters.keys())
                }
            }
        }

def tool(func=None, *, name=None, description=None):
    def decorator(func):
        tool_instance = Tool(name or func.__name__, description or func.__doc__, func)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return tool_instance.execute(*args, **kwargs)

        wrapper._tool = tool_instance
        return wrapper
    if func is None:
        return decorator
    return decorator(func)
