"""Creates the source code of a new LangChain Tool on-the-fly and writes it into session cwd."""
import os
import re

from pydantic import BaseModel

from yeagerai.core.y_tool import YeagerTool

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)


class CreateToolSourceAPIWrapper(BaseModel):
    session_path: str
    openai_api_key: str = os.getenv("OPENAI_API_KEY")

    def run(self, query: str) -> str:
        # Initialize ChatOpenAI with API key and model name
        chat = ChatOpenAI(
            openai_api_key=self.openai_api_key, model_name="gpt-3.5-turbo"
        )

        # Read the master prompt template file
        with open(
            "yeagerai/agents/y_agent_builder/kit/create_tool_source/create_tool_master_prompt.md",
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
        out = chain.run(product=query)

        # Parse the Python block inside the output, handling different code block formats
        code_block_pattern = re.compile(r"(```.*?```)", re.DOTALL)
        code_block = re.search(code_block_pattern, out)
        if code_block:
            code = code_block.group(1).strip()

            if code.startswith("```python"):
                code = code[9:]
            elif code.startswith("```"):
                code = code[3:]

            if code.endswith("```"):
                code = code[:-3]

            # Extract the name of the class from the code block
            class_name_pattern = re.compile(r"class (\w+)\(BaseModel\):")
            class_name_match = re.search(class_name_pattern, code)
            if class_name_match:
                class_name = class_name_match.group(1)

                # Write the {class_name}.py file inside the user-defined session_path
                output_file = f"{class_name}.py"
                with open(os.path.join(self.session_path, output_file), "w") as f:
                    f.write(code)
                    f.close()

                return f"The file {class_name}.py has been written in the {self.session_path} successfully!\nHere is the source code of the {class_name} LangChain tool based on given requirements:\n{code}"

        return "Error: No code block found or class name could not be extracted."


class CreateToolSourceRun(YeagerTool):
    """Tool that adds the capability of creating the source code of other Tools on-the-fly and writing it into cwd."""

    name = "Create Tool Source"
    description = """Useful for when you need to create a LangChain Tool. 
        Input should be two strings, the first string represents the prompt explaining the functionality wanted in the Tool,
        and the second string is the session_path defined earlier in the conversation.
        For example, [\"A tool that adds the capability of creating the source code of other Tools on-the-fly and writing it into cwd.\",\"./my_tools\"]"""
    final_answer_format = (
        "Final answer: just return the output code block and a success message"
    )
    api_wrapper: CreateToolSourceAPIWrapper

    def _run(self, query: str) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("GoogleSearchRun does not support async")
