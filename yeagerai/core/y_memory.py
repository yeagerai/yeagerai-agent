from langchain.memory import ConversationSummaryBufferMemory, ConversationEntityMemory, CombinedMemory
class YeagerContextMemory(CombinedMemory):
    """Memory for the Yeager agent."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #short term memory, last 10 interactions
        
        # session entitiy memory (needs chroma)
        
        # load pinecone memory of the most similar interactions to the question of the current interaction of the same user and thread

        # load from shared infinite context memory pinecone most relevant interactions to the question topic with various formats
            # solution sketches
            # code snippets
            # api docs



