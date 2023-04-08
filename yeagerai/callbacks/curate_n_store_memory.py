import os
import json
from typing import Any, Dict, Optional, Union

import openai
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult
from pinecone import PineconeClient

class PineconeCallbackHandler(BaseCallbackHandler):
    """Callback Handler that stores information in Pinecone and manages interactions."""

    def __init__(self, session_id: str) -> None:
        """Initialize callback handler."""
        super().__init__()

        self.session_id = session_id
        self.pinecone_client = PineconeClient()

        # Initialize Pinecone namespace
        self.pinecone_client.create_namespace(namespace=self.session_id)

    def _get_gpt_summary_and_entities(self, text: str) -> Dict[str, str]:
        # Create a prompt for summary and entities extraction
        prompt = f"Create a summary of the following text and extract the entities and their values:\n\n{text}\n\nSummary:{{summary}}{{entities}}"

        # Call the GPT API with the prompt
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=["{{summary}}", "{{entities}}"],
            temperature=0.5,
        )

        # Extract the summary and entities from the GPT API response
        text = response.choices[0].text.strip()
        summary, entities = text.split("{{summary}}")[1].split("{{entities}}")

        return {"summary": summary.strip(), "entities": entities.strip()}

    def _store_interactions(self, interaction: str) -> None:
        # Store interaction in a text file
        interactions_file = os.path.join(self.session_path, "last_10_interactions.txt")

        if not os.path.exists(interactions_file):
            with open(interactions_file, "w") as f:
                f.write(interaction)
        else:
            with open(interactions_file, "r") as f:
                interactions = f.readlines()

            # Keep only the last 10 interactions
            interactions.append(interaction)
            interactions = interactions[-10:]

            with open(interactions_file, "w") as f:
                f.writelines(interactions)

    def on_agent_start(self, **kwargs: Any) -> None:
        # Load the memory and entities from Pinecone
        memory_and_entities = self.pinecone_client.fetch(key=self.session_id, namespace=self.session_id)

        if memory_and_entities:
            # Deserialize and load the memory and entities
            memory_and_entities = json.loads(memory_and_entities)
            memory = memory_and_entities.get('memory', None)
            entities = memory_and_entities.get('entities', None)

            # Load the memory into langchain (replace with the actual function to load memory)

            # Load the entities into langchain (replace with the actual function to load entities)

        # Load the last_10_interactions.txt file into langchain memory
        interactions_file = os.path.join(self.session_path, "last_10_interactions.txt")

        if os.path.exists(interactions_file):
            with open(interactions_file, "r") as f:
                last_10_interactions = f.read()
            # Load the last_10_interactions into langchain memory (replace with the actual function)

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        # Get the overall interaction text from the AgentFinish object
        interaction_text = str(finish)  # Replace with the actual way to get the interaction text

        # Call GPT API to create a summary and extract entities
        summary_and_entities = self._get_gpt_summary_and_entities(interaction_text)

        # Store the information in Pinecone
        self.pinecone_client.upsert(
            key=self.session_id,
            value=json.dumps(summary_and_entities),
            namespace=self.session_id
        )

        # Store the last interaction in a text file
        self._store_interactions(interaction_text)