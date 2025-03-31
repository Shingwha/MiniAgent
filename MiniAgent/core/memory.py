from pydantic import BaseModel
from typing import Dict

class Memory(BaseModel):
    type: str
    id: str
    title: str
    content: str
    created_time: Dict

    def __init__(self, **data):
        super().__init__(**data)

    def __str__(self):
        return f"Memory(id={self.id},type={self.type}, title={self.title}, content={self.content}, created_time={self.created_time})"



class MemoryBank(BaseModel):
    memories: list[Memory]

    def __init__(self, **data):
        super().__init__(**data)

    def __str__(self):
        return f"MemoryBank(memories={self.memories})"

    def add_memory(self, memory: Memory):
        self.memories.append(memory)

    def remove_memory(self, memory: Memory):
        self.memories.remove(memory)

    def count(self):
        return len(self.memories)
    
    def clear(self):
        self.memories.clear()
    
    def get_memory_by_id(self, id: str) -> Memory:
        for memory in self.memories:
            if memory.id == id:
                return memory
        return None
    
    def get_memory_by_type(self, type: str) -> list[Memory]:
        memories = []
        for memory in self.memories:
            if memory.type == type:
                memories.append(memory)
        return memories
    
    def get_memory_by_time(self, start_time: str, end_time: str) -> list[Memory]:
        memories = []
        for memory in self.memories:
            if start_time <= memory.created_time <= end_time:
                memories.append(memory)
        return memories


