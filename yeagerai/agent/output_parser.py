import re
from typing import Union

from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentOutputParser

def treat_reflections_and_strategy():
    # Move that to the KageBunshin callback for updating the context based on the reflection and strategy
    pass


class YeagerAIOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        if "Feedback Request:" in llm_output:
            treat_reflections_and_strategy()
            return AgentFinish(
                return_values={"output": llm_output.split("Feedback Request:")[-1].strip()},
                log=llm_output,
            )

        if "Final Answer:" in llm_output:
            treat_reflections_and_strategy()
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)

        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input, log=llm_output)
