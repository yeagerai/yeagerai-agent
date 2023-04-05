import os
import re

from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

from pydantic import BaseModel
class CreateToolSource(BaseModel):
    openai_api_key: str
    output_path: str

    def run(self, command:str) -> str:
        load_dotenv()

        chat = ChatOpenAI(
            openai_api_key=self.openai_api_key, model_name="gpt-3.5-turbo"
        )

        with open("create_tool_master_prompt.md", "r") as f:
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
    

