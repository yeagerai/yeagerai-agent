from langchain.agents import Tool
from yeagerai.core.y_kit import YeagerKit
from yeagerai.y_kits_lib.tool_creation_kit.create_tool_source.create_tool_source import CreateToolSource


tckit = YeagerKit()

tckit.register_tool(
        Tool(
            name = "CreateToolSource",
            func=CreateToolSource.run,
            description="This tool creates a new tool source python snippet.",
            return_direct=True
        )
    )
