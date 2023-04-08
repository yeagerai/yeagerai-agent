import os
import uuid
from typing import Any, Dict, Optional, Union

from git import Repo, Actor
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult

class GitLocalRepoCallbackHandler(BaseCallbackHandler):
    """Callback Handler that creates a local git repo and commits changes."""

    def __init__(self, username: str) -> None:
        """Initialize callback handler."""
        super().__init__()

        # Generate a UUID for the session
        session_id = str(uuid.uuid4())

        # Set the session_path using UUID and username
        self.session_path = os.path.join(session_id, username)

        # Create the local git repo
        os.makedirs(self.session_path, exist_ok=True)
        self.repo = Repo.init(self.session_path)
        self.committer = Actor(username, f"{username}@example.com")

    def _get_gpt_commit_message(self, repo: Repo) -> str:
        """
        Call the GPT API to get a commit message that explains the differences.
        """
        # Get the differences
        diff_output = repo.git.diff(repo.head.commit.tree)

        # Create a prompt template
        prompt_tempalte = "Explain the following changes in a Git commit message:\n\n{diff_output}\n\nCommit message:"

        # Call the GPT API with the prompt (replace by langchain LLM)
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the commit message from the GPT API response
        commit_message = response.choices[0].text.strip()

        return commit_message

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Commit changes when an agent finishes its execution."""
        self.repo.git.add(A=True)

        if self.repo.is_dirty():
            commit_message = self._get_gpt_commit_message(self.repo)
            self.repo.index.commit(commit_message, author=self.committer, committer=self.committer)
