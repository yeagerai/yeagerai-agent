from typing import List
from langchain.prompts import BaseChatPromptTemplate
from langchain.schema import HumanMessage, BaseMessage

from yeagerai.toolkit import YeagerAITool

class YeagerAIPromptTemplate(BaseChatPromptTemplate):
    template: str
    tools: List[YeagerAITool]
    session_summary: str

    def format_messages(self, **kwargs) -> List[BaseMessage]:
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "

        kwargs["agent_scratchpad"] = thoughts

        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools]
        )
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        kwargs["tools_final_answer_formats"] = "\n    - ".join(
            [tool.name + ": " + tool.final_answer_format for tool in self.tools]
        )

        kwargs["session_summary"] = self.session_summary

        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]