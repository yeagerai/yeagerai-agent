import os
from typing import Any

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentFinish

from yeagerai.memory import YeagerAIContext


class KageBunshinNoJutsu(BaseCallbackHandler):
    """Callback Handler is used to handle safe and load memory tasks."""

    def __init__(
        self, context_memory: YeagerAIContext
    ) -> None:
        """Initialize callback handler."""
        super().__init__()
        self.context_memory = context_memory
        self.context_memory.create_shadow_clones()

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Save memory when agent finishes."""
        self.context_memory.dispell_shadow_clones()
        self.context_memory.create_shadow_clones()

    def on_agent_action(self):
        pass

    def on_chain_end(self):
        pass

    def on_chain_error(self):
        pass

    def on_chain_start(self):
        pass

    def on_llm_end(self):
        pass

    def on_llm_error(self):
        pass

    def on_llm_new_token(self):
        pass

    def on_llm_start(self):
        pass

    def on_text(self):
        pass

    def on_tool_end(self):
        pass

    def on_tool_error(self):
        pass

    def on_tool_start(self):
        pass
