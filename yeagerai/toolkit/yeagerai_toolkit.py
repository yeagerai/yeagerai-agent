"""Toolkit for interacting with the YeagerAI tools."""
from __future__ import annotations

from typing import List

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool
from yeagerai.toolkit.yeagerai_tool import YeagerTool

class YeagerAIToolkit(BaseToolkit):
    """Toolkit for interacting with a JSON spec."""


    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
        ]
    
    def register_tool(self, tool: BaseTool):
        """Register a tool to the toolkit."""
        pass