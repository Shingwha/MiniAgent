from ..core import Tool

class MemoryTool(Tool):
    def __init__(self):
        super().__init__(
            name="MemoryTool",
            description="""
            当用户需要查看关于记忆的情况，可以调用此工具。
            可以执行的操作有：
            1.search_recent_memory: 查看最近的记忆
            2.search_memory_by_date: 根据日期搜索简略的记忆
            3.search_memory_by_type: 根据记忆类型搜索简略的记忆
            4.search_memory_by_id: 根据记忆ID搜索精确的记忆
            5.add_memory: 添加新的记忆
            6.delete_memory: 删除记忆
            """,
            func=self.memory_process,
        )

    def memory_process(self,process_type,memory_type,memory_id,start_date,end_date,memory_content):
        if process_type == "search_recent_memory":
            self.search_recent_memory()
        elif process_type == "search_memory_by_date":
            self.search_memory_by_date(start_date,end_date)
        elif process_type == "search_memory_by_type":
            self.search_memory_by_type(memory_type)
        elif process_type == "search_memory_by_id":
            self.search_memory_by_id(memory_id)
        elif process_type == "add_memory":
            self.add_memory(memory_type,memory_content)
        elif process_type == "delete_memory":
            self.delete_memory(memory_id)

    def search_recent_memory(self):
        pass

    def search_memory_by_date(self):
        pass

    def search_memory_by_type(self):
        pass

    def search_memory_by_id(self):
        pass

    def add_memory(self):
        pass

    def delete_memory(self):
        pass
        