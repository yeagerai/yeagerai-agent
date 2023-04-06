from langchain.agents import Tool

class YeagerProtocol(Tool):
    def __init__(self, name, func, description, return_direct=False):
        super().__init__(name, func, description, return_direct)
        self.name = name
        self.func = func
        self.description = description
        self.return_direct = return_direct

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)    