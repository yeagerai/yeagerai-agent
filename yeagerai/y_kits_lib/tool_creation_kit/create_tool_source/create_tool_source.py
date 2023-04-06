import os
import re

from dotenv import load_dotenv

from pydantic import BaseModel

from langchain.tools.base import BaseTool

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

class CreateToolSourceAPIWrapper(BaseModel):

    def run(self, command:str) -> str:
        load_dotenv()

        chat = ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-3.5-turbo"
        )

        with open("yeagerai/y_kits_lib/tool_creation_kit/create_tool_source/create_tool_master_prompt.md", "r") as f:
            template_prompt = f.read()
            f.close()

        input_variables = list(map(lambda x: x[1:-1], re.findall(r"\{.+\}", template_prompt)))
        
        y_tool_master_prompt = PromptTemplate(
            input_variables=input_variables,
            template=template_prompt,
        )

        human_message_prompt = HumanMessagePromptTemplate(prompt=y_tool_master_prompt)
        chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])
        chain = LLMChain(llm=chat, prompt=chat_prompt)
        out = chain.run(
            product=command
        )
        
        # parse the python block inside

        # extract the name of the class from the code block

        # write the {class_name}.py file inside the output_path

        return out # the file name has been written
    


class CreateToolSourceRun(BaseTool):
    """Tool that adds the capability to query the Google search API."""

    name = "Create Tool Source"
    description = (
        "A wrapper around Google Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    api_wrapper: CreateToolSourceAPIWrapper

    def _run(self, query: str) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("GoogleSearchRun does not support async")