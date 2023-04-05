from typing import Any, Dict, List, Optional, Union


from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult


class DiscordCallbackHandler(BaseCallbackHandler):
    """Callback Handler that logs to Discord."""
    def __init__(self, discord_bot_instance:Any) -> None:
        """Initialize the Discord bot."""
        self.bot = discord_bot_instance

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Print out the prompts."""

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Stream the new token to the discord channel."""
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Thanks for using the Yeager Agent Builder!"""
        pass

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Sorry, I'm experiencing errors with my internal LLM, do you want to retry?."""
        pass

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        pass

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        pass

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        pass

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        """Does the user have free credits in our DB? Else send the webpage link so theyt can pay.
        If they have, then remove 1 credit from the DB and continue.
        """
        pass

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action.
        It depends on the action, different embed types and forms depending on the actions
        """
        pass

    def on_tool_end(
        self,
        output: str,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""
        pass

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        pass

    def on_text(self, text: str, **kwargs: Any) -> None:
        """Run on text."""
        pass

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent end."""
        pass