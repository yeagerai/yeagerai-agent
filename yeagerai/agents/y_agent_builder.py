from yeagerai.core.y_kit import YeagerKit
from yeagerai.y_kits_lib.tool_creation_kit.create_tool_source.create_tool_source import (
    CreateToolSourceRun,
    CreateToolSourceAPIWrapper,
)
from yeagerai.core.y_base_agent import YeagerBaseAgent

tckit = YeagerKit()

tckit.register_tool(CreateToolSourceRun(api_wrapper=CreateToolSourceAPIWrapper()))

y_agent_builder = YeagerBaseAgent(
    name="yAgentBuilder",
    description="A Yeager.ai agent that uses Yeager.ai's agent creation kit to create custom LangChain agents from prompts.",
    openai_model_name="gpt-3.5-turbo",
    yeager_kit=tckit,
)
