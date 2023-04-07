from dotenv import load_dotenv

from yeagerai.core.y_kit import YeagerKit
from yeagerai.y_kits_lib.tool_creation_kit.create_tool_source.create_tool_source import (
    CreateToolSourceRun,
    CreateToolSourceAPIWrapper,
)
from yeagerai.y_kits_lib.tool_creation_kit.start_session_git_directory.start_session_git_directory import (
    StartSessionTool,
    StartSessionToolAPIWrapper,
)
from yeagerai.core.y_base_agent import YeagerBaseAgent

load_dotenv()

tckit = YeagerKit()

tckit.register_tool(CreateToolSourceRun(api_wrapper=CreateToolSourceAPIWrapper()))
tckit.register_tool(StartSessionTool(api_wrapper=StartSessionToolAPIWrapper()))

y_agent_builder = YeagerBaseAgent(
    name="yAgentBuilder",
    description="A Yeager.ai agent that uses Yeager.ai's agent creation kit to create custom LangChain agents from prompts.",
    openai_model_name="gpt-4",
    yeager_kit=tckit,
)
