import os
import json

from langchain.schema import messages_from_dict, messages_to_dict
from langchain.memory import (
    ConversationBufferMemory,
    ChatMessageHistory,
    ConversationSummaryBufferMemory,
)
from langchain.llms import OpenAI
from langchain.document_loaders import ReadTheDocsLoader
"""
YeagerAI Documentation: {yeager_docs}
LangChain Documentation: {langchain_docs}
Additional Data Sources: {data_sources}
"""

class YeagerAIContext:
    """Context for the @yeager.ai agent."""

    def __init__(self, username: str, session_id: str, session_path: str):
        self.username = username
        self.session_id = session_id
        self.session_path = session_path
        self.llm = OpenAI()
        self.session_message_history = ChatMessageHistory()
        self.chat_buffer_memory = ConversationBufferMemory(
            memory_key="chat_history", input_key="input"
        )
        self.conv_summary = ConversationSummaryBufferMemory(
            llm=self.llm, memory_key="conversation_summary", input_key="input", max_token_limit=1000
        )

        self.yeager_docs_db_connector = ""
        self.langchain_docs_db_connector = ""
        self.pinecone_docs_db_connector = ""
        self.chroma_docs_db_connector = ""



    def load_session_message_history(self):
        try:
            with open(os.path.join(self.session_path, "session_history.txt"), "r") as f:
                dicts = json.loads(f.read())
                self.session_message_history.messages = messages_from_dict(dicts)
        except FileNotFoundError:
            os.makedirs(self.session_path, exist_ok=True)
            with open(os.path.join(self.session_path, "session_history.txt"), "w") as f:
                f.close()

    def save_session_message_history(self):
        dicts = messages_to_dict(self.session_message_history.messages)
        with open(os.path.join(self.session_path, "session_history.txt"), "w") as f:
            f.write(json.dumps(dicts))
            f.close()

    def create_shadow_clones(self):
        self.load_session_message_history()
        self.chat_buffer_memory.chat_memory = self.session_message_history
        self.conv_summary.chat_memory = self.session_message_history

    def dispell_shadow_clones(self):
        self.session_message_history = self.chat_buffer_memory.chat_memory
        self.save_session_message_history()
