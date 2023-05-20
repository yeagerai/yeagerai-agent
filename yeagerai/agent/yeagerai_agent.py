from typing import List, Callable

from pydantic import BaseModel

from langchain import LLMChain
from langchain.agents import AgentExecutor, LLMSingleActionAgent
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import CallbackManager

from yeagerai.toolkit import YeagerAIToolkit
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
        model_type: str,
        model_name: str,
        request_timeout: int,
        callbacks: List[Callable],
        context: YeagerAIContext,
        yeager_kit: YeagerAIToolkit,
    ):
        self.username = username
        self.session_id = session_id
        self.session_path = session_path
        self.model_name = model_name
        self.model_type = model_type
        self.request_timeout = request_timeout
        self.callbacks = callbacks
        self.context = context
        self.yeager_kit = yeager_kit

        self.prompt = YeagerAIPromptTemplate(
            template=MASTER_TEMPLATE,
            tools=self.yeager_kit.get_tools(),
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=["input", "intermediate_steps"],
            chat_history=self.context.chat_buffer_memory.chat_memory,
        )
        
        llm_args = {
            "ChatOpenAI": {
                "temperature":0.2,
                "model_name":       self.model_name,
                "request_timeout":  self.request_timeout,
            }
        }
        
        llm = SimpleLLMFactory(
            self.model_type,
            kwargs = llm_args.get(self.model_type,{})
            )
        
        self.llm_chain = LLMChain(
            llm=llm,
            prompt=self.prompt,
            memory=self.context.chat_buffer_memory,
            callback_manager=CallbackManager(self.callbacks),
            verbose=True,
        )

        self.output_parser = YeagerAIOutputParser()

        self.agent = LLMSingleActionAgent(
            llm_chain=self.llm_chain,
            output_parser=self.output_parser,
            stop=["\nObservation:"],
        )
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.yeager_kit.get_tools(),
            verbose=True,
        )

    def run(self, input):
        try:
            return self.agent_executor.run(input)
        except ValueError:
            return "Final answer: some issues were found while parsing the output."
