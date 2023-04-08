from dotenv import load_dotenv

from yeagerai.core.y_kit import YeagerKit
from yeagerai.agents.y_agent_builder.kit.create_tool_source.create_tool_source import (
    CreateToolSourceRun,
    CreateToolSourceAPIWrapper,
)
from yeagerai.core.y_memory import YeagerMemory
from yeagerai.core.y_base_agent import YeagerBaseAgent
from yeagerai.callbacks.curate_n_store_memory import CurateNStoreMemory
from yeagerai.callbacks.git_local_repo import GitLocalRepo

load_dotenv()

# instantiate the YeagerMemory and load LTM
memory = YeagerMemory()

# instantiate the YeagerKit
tckit = YeagerKit()
tckit.register_tool(CreateToolSourceRun(api_wrapper=CreateToolSourceAPIWrapper()))

y_agent_builder = YeagerBaseAgent(
    name="yAgentBuilder",
    description="A Yeager.ai agent that uses Yeager.ai's agent creation kit to create custom LangChain agents from prompts.",
    preffix_template="",
    suffix_template="",
    openai_model_name="gpt-4",
    yeager_kit=tckit,
    memory=memory,
    callbacks=[CurateNStoreMemory(), GitLocalRepo()],
)
