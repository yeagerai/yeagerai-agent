"""Util that starts a working session."""
import os

from git import Repo
from pydantic import BaseModel
from yeagerai.core.y_tool import YeagerTool

class StartSessionToolAPIWrapper(BaseModel):
    """A tool that starts a working session.
    This tool does not have any external dependencies and simply starts a working session.
    """
    def run(self, query: str) -> str:
        """Start a working session and return a confirmation message."""
        # remove the " signs
        query = query.replace("\"","").strip() 
        
        if os.path.isabs(os.path.abspath(query)):
            path = os.path.abspath(query)
        else:
            return "Please provide a real path. The input provided is not a valid path."

        os.makedirs(path, exist_ok=True)
        Repo.init(path)

        return f"Working session started successfully, the session_path is {path}."

class StartSessionTool(YeagerTool):
    """Tool that starts the working session path and creates a git repository on this path."""

    name = "Start Session"
    description = (
        """This tool usually will be called as the first action of the agent. It basically sets the cwd named session_path for the whole conversation. 
        Input is a string which will be the session_path.
        For example, \"./my_tools\""""
    )
    final_answer_format = "Final answer: just return the output session_path and a success message"
    api_wrapper: StartSessionToolAPIWrapper

    def _run(self, query: str) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("GoogleSearchRun does not support async")