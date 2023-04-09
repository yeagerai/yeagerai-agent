from typing import List, Callable

from langchain import LLMChain
from langchain.agents import AgentExecutor, LLMSingleActionAgent
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import CallbackManager

from yeagerai.toolkit import (
    YeagerAIToolkit,
    CreateToolSourceAPIWrapper,
    CreateToolSourceRun,
    DesignSolutionSketchAPIWrapper,
    DesignSolutionSketchRun,
    CreateToolMockedTestsAPIWrapper,
    CreateToolMockedTestsRun,
)
from yeagerai.memory import YeagerAIContext
from yeagerai.agent.output_parser import YeagerAIOutputParser
from yeagerai.agent.prompt_template import YeagerAIPromptTemplate
from yeagerai.agent.master_template import MASTER_TEMPLATE


class YeagerAIAgent:
    name: str = "yeager.ai"
    description: str = "The ultimate LangChain Agent Builder."

    def __init__(
        self,
        username: str,
        session_id: str,
        session_path: str,
        model_name: str,
        request_timeout: int,
        streaming: bool,
        callbacks: List[Callable],
        context: YeagerAIContext,
    ):
        self.username = username
        self.session_id = session_id
        self.session_path = session_path
        self.model_name = model_name
        self.request_timeout = request_timeout
        self.streaming = streaming
        self.callbacks = callbacks
        self.context = context

        # build toolkit
        self.yeager_kit = YeagerAIToolkit()
        self.yeager_kit.register_tool(
            DesignSolutionSketchRun(
                api_wrapper=DesignSolutionSketchAPIWrapper(
                    session_path=self.session_path,
                    model_name=self.model_name,
                    request_timeout=self.request_timeout,
                    streaming=self.streaming,
                )
            ),
        )
        self.yeager_kit.register_tool(
            CreateToolMockedTestsRun(
                api_wrapper=CreateToolMockedTestsAPIWrapper(
                    session_path=self.session_path,
                    model_name=self.model_name,
                    request_timeout=self.request_timeout,
                    streaming=self.streaming,
                )
            ),
        )
        self.yeager_kit.register_tool(
            CreateToolSourceRun(
                api_wrapper=CreateToolSourceAPIWrapper(
                    session_path=self.session_path,
                    model_name=self.model_name,
                    request_timeout=self.request_timeout,
                    streaming=self.streaming,
                )
            ),
        )

        self.prompt = YeagerAIPromptTemplate(
            template=MASTER_TEMPLATE,
            tools=self.yeager_kit.get_tools(),
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=["input", "intermediate_steps"],
            chat_history=self.context.chat_buffer_memory.chat_memory,
        )

        self.llm_chain = LLMChain(
            llm=ChatOpenAI(
                temperature=0.2,
                model_name=self.model_name,
                request_timeout=self.request_timeout,
                streaming=self.streaming,
            ),
            prompt=self.prompt,
            memory=self.context.chat_buffer_memory,
            callback_manager=CallbackManager(self.callbacks),
            verbose=True,
        )

        self.output_parser = YeagerAIOutputParser()

        tool_names = [tool.name for tool in self.yeager_kit.get_tools()]
        self.agent = LLMSingleActionAgent(
            llm_chain=self.llm_chain,
            output_parser=self.output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names,
        )
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent, tools=self.yeager_kit.get_tools(), verbose=True,
        )

    def run(self, input):
        try:
            return self.agent_executor.run(input)
        except ValueError:
            return "Final answer: some issues were found while parsing the output."
