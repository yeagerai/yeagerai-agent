from langchain.agents import Tool
from yeagerai.core.y_kit import YeagerKit
from yeagerai.y_kits_lib.tool_creation_kit.create_tool_source.create_tool_source import (
    CreateToolSourceRun,
    CreateToolSourceAPIWrapper,
)


tckit = YeagerKit()

tckit.register_tool(CreateToolSourceRun(api_wrapper=CreateToolSourceAPIWrapper()))
