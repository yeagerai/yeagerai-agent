from typing import List, Callable

from langchain import LLMChain
from langchain.agents import AgentExecutor, LLMSingleActionAgent
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import CallbackManager

from yeagerai.toolkit import YeagerAIToolkit
from yeagerai.memory import YeagerAIContext
from yeagerai.agent import MASTER_TEMPLATE, YeagerAIOutputParser, YeagerAIPromptTemplate

class YeagerAIAgent:
    name:str = "yeager.ai"
    description:str = "The ultimate LangChain Agent Builder."

    def __init__(self, username: str, session_id:str, session_path:str, callbacks: List[Callable], context: YeagerAIContext):

        self.username = username
        self.session_id = session_id
        self.session_path = session_path
        self.callbacks = callbacks
        self.context = context

        # build toolkit
        self.yeager_kit = YeagerAIToolkit()
        self.yeager_kit.register_tools([

        ])

        self.prompt = YeagerAIPromptTemplate(
            template=MASTER_TEMPLATE,
            tools=self.yeager_kit.get_tools(),
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=["input", "intermediate_steps"],
        )

        self.llm_chain = LLMChain(
            llm=ChatOpenAI(temperature=0.2, model_name="gpt-4"),
            prompt=self.prompt,
            memory=self.context.chat_buffer_memory,
            callback_manager=CallbackManager(self.callbacks),
        )

        self.output_parser = YeagerAIOutputParser()

        tool_names = [tool.name for tool in self.kit.tools]
        self.agent = LLMSingleActionAgent(
            llm_chain=self.llm_chain,
            output_parser=self.output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names,
        )
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent, tools=self.yeager_kit.get_tools(), verbose=True
        )

    def run(self, input):
        return self.agent_executor.run(input)
