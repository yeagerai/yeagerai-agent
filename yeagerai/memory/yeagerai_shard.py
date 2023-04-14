from typing import List
from uuid import uuid4
from langchain.embeddings import OpenAIEmbeddings
from chromadb.api.local import LocalAPI
from chromadb.api.fastapi import FastAPI

class YeagerAIShard:
    embeddings = OpenAIEmbeddings()
    def __init__(self,username: str, session_id: str, document: str, type:str):
        self.id = uuid4()
        self.username = username
        self.session_id = session_id
        self.document = document
        self.embedding = self.embeddings.embed_query(self.document)
        self.type = type

    @classmethod
    def from_database(cls, connector: (LocalAPI | FastAPI), id: str):
        shard = connector._get(ids=[id])
        return cls(
            username=shard.metadata["username"],
            session_id=shard.metadata["session_id"],
            document=shard.document,
            type=shard.metadata["type"],
        )

    def send_shard(self, connector: (LocalAPI | FastAPI)):
        connector.add(
            embeddings=[self.embedding],
            metadatas=[{"username": self.username, "session_id": self.session_id, "type": self.type}],
            documents=[self.document],
            ids=[self.id],
        )
