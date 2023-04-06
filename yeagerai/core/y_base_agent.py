from typing import List

from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain import OpenAI, LLMChain
from langchain.prompts import BaseChatPromptTemplate
from langchain.schema import HumanMessage

# Set up the base template
template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question. This Final Answer, have a format based on the tool you used. The possible formats are
{tools_final_answer_formats}

Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Arg"s

Question: {input}
{agent_scratchpad}
"""


# Set up a prompt template
class YeagerBasePromptTemplate(BaseChatPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

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
            [tool.final_answer_format for tool in self.tools]
        )

        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]


class YeagerBaseAgent:
    def __init__(self, name, openai_model_name, description, yeager_kit):
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
        # self.output_parser = CustomOutputParser()

        tool_names = [tool.name for tool in self.kit.tools]
        self.agent = LLMSingleActionAgent(
            llm_chain=self.llm_chain,
            # output_parser=self.output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names,
        )
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent, tools=self.kit.tools, verbose=True
        )

    def run(self, input):
        return self.agent_executor.run(input)
