import os
from typing import Any

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentFinish

from yeagerai.core.y_memory import YeagerContextMemory


class MemoryCallbackHandler(BaseCallbackHandler):
    """Callback Handler is used to handle safe and load memory tasks."""

    def __init__(
        self, username: str, session_path: str, context_memory: YeagerContextMemory
    ) -> None:
        """Initialize callback handler."""
        super().__init__()
        self.username = username
        self.session_path = session_path
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.context_memory = context_memory
        self.context_memory.load_memory()

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Save memory when agent finishes."""
        self.context_memory.store_session_history()
        self.context_memory.load_memory()

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
