"""Creates the source code of a new LangChain Tool on-the-fly and writes it into session cwd."""
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
    def run(self, command: str, session_path: str) -> str:
        # Load environment variables
        load_dotenv()

        # Initialize ChatOpenAI with API key and model name
        chat = ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-3.5-turbo"
        )

        # Read the master prompt template file
        with open(
            "yeagerai/y_kits_lib/tool_creation_kit/create_tool_source/create_tool_master_prompt.md",
            "r",
        ) as f:
            template_prompt = f.read()
            f.close()

        # Create a PromptTemplate instance with the read template
        y_tool_master_prompt = PromptTemplate(
            input_variables=["product"],
            template=template_prompt,
        )

        # Create a HumanMessagePromptTemplate instance with the master prompt
        human_message_prompt = HumanMessagePromptTemplate(prompt=y_tool_master_prompt)
        chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])

        # Create an LLMChain instance and run the command
        chain = LLMChain(llm=chat, prompt=chat_prompt)
        out = chain.run(product=command)

        # Parse the Python block inside the output, handling different code block formats
        code_block_pattern = re.compile(
            r"(?:```(?:python)?\s*)?(class .*?)(?:```)?", re.DOTALL
        )
        code_block = re.search(code_block_pattern, out)
        if code_block:
            code = code_block.group(1).strip()

            # Extract the name of the class from the code block
            class_name_pattern = re.compile(r"class (\w+):")
            class_name_match = re.search(class_name_pattern, code)
            if class_name_match:
                class_name = class_name_match.group(1)

                # Write the {class_name}.py file inside the user-defined session_path
                output_file = f"{class_name}.py"
                with open(os.path.join(session_path, output_file), "w") as f:
                    f.write(code)
                    f.close()

                return f"The file {class_name}.py has been written in the {session_path} successfully!"

        return "Error: No code block found or class name could not be extracted."


class CreateToolSourceRun(BaseTool):
    """Tool that adds the capability of creating the source code of other Tools on-the-fly and writing it into cwd."""

    name = "Create Tool Source"
    description = (
        "A wrapper around CreateToolSourceAPIWrapper. "
        "Useful for when you need to create a LangChain Tool. "
        "Input should be a prompt explaining the functionality wanted in the Tool."
    )
    api_wrapper: CreateToolSourceAPIWrapper

    def _run(self, query: str) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("GoogleSearchRun does not support async")
