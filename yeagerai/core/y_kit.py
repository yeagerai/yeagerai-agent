from langchain.agents import Tool

from yeagerai.core.y_protocol import YeagerProtocol

class YeagerKit:
    def __init__(self):
        self.tools = []
        self.protocols = []

    def register_tool(self, tool: Tool):
        self.tools.append(tool)

    def get_tools(self):
        return self.tools

    def register_protocol(self, protocol: YeagerProtocol):
        self.tools.append(protocol)

    def get_protocols(self):
        return self.protocols