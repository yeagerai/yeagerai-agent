import re
from typing import List, Union

from langchain.agents import AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.schema import AgentAction, AgentFinish, HumanMessage
from langchain import OpenAI, LLMChain
from langchain.prompts import BaseChatPromptTemplate
from langchain.schema import HumanMessage

from yeagerai.core.y_tool import YeagerTool

# Set up the base template
template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

ALWAYS use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought -> Action + Action Input -> Observation can repeat N times)

Final Answer: the final answer to the original input question. This Final Answer, have a format based on the tool you used. The possible formats which depend on the tool that you are using are
{tools_final_answer_formats}

Question: {input}
{agent_scratchpad}
"""


# Set up a prompt template
class YeagerBasePromptTemplate(BaseChatPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[YeagerTool]

    def format_messages(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools]
        )
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])

        # Create a list of tool final formats for the tools provided
        kwargs["tools_final_answer_formats"] = "\n    - ".join(
            [tool.name +": "+ tool.final_answer_format for tool in self.tools]
        )

        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]

class CustomOutputParser(AgentOutputParser):
    
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)

        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input, log=llm_output)

class YeagerBaseAgent:
    def __init__(self, name, description, openai_model_name, yeager_kit):
        self.name = name
        self.description = description
        self.kit = yeager_kit

        self.prompt = YeagerBasePromptTemplate(
            template=template,
            tools=self.kit.tools,
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=["input", "intermediate_steps"],
        )

        self.llm_chain = LLMChain(
            llm=OpenAI(temperature=0, model_name=openai_model_name), prompt=self.prompt
        )
        self.output_parser = CustomOutputParser()

        tool_names = [tool.name for tool in self.kit.tools]
        self.agent = LLMSingleActionAgent(
            llm_chain=self.llm_chain,
            output_parser=self.output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names,
        )
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent, tools=self.kit.tools, verbose=True
        )

    def run(self, input):
        return self.agent_executor.run(input)
