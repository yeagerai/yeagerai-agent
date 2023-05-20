"""Toolkit for interacting with the YeagerAI tools."""
from __future__ import annotations

from typing import List

from langchain.agents.agent_toolkits.base import BaseToolkit
from yeagerai.toolkit.yeagerai_tool import YeagerAITool


class YeagerAIToolkit(BaseToolkit):
    """Toolkit for interacting with a JSON spec."""

    def __init__(self) -> None:
        self.tools_list: List[YeagerAITool] = []

    def get_tools(self) -> List[YeagerAITool]:
        """Get the tools in the toolkit."""
        return self.tools_list

    def register_tool(self, tool: YeagerAITool):
        """Register a tool to the toolkit."""
        self.tools_list.append(tool)
