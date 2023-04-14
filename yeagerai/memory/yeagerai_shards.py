from typing import List
from uuid import uuid4
from langchain.embeddings import OpenAIEmbeddings

"""
Conversation Summary: {conv_summary}
Conversation Rolling Window: {conv_rolling_window}
Available Tools: {tools}
YeagerAI Documentation: {yeager_docs}
LangChain Documentation: {langchain_docs}
Additional Data Sources: {data_sources}
"""
# add and query shards from callback
class YeagerAIShard:
    embeddings = OpenAIEmbeddings()
    def __init__(self,username: str, session_id: str, document: str):
        self.id = uuid4()
        self.document = document
        self.embedding = self.embeddings.embed_query(self.document)
        self.metadata = {}
        self.metadata["username"] = username
        self.metadata["session_id"] = session_id

    @classmethod
    def from_database(cls, connector: (LocalAPI | FastAPI), id: str):
        shard = connector._get(ids=[id])
        return cls(
            username=shard.metadata["username"],
            session_id=shard.metadata["session_id"],
            document=shard.document,
            metadata=shard.metadata,
        )

    def send_shard(self, connector: (LocalAPI | FastAPI)):
        connector.add(
            embeddings=[self.embedding],
            metadatas=[{"username": self.username, "session_id": self.session_id, "type": self.type}],
            documents=[self.document],
            ids=[self.id],
        )
