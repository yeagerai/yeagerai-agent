class YeagerContextMemory(CombinedMemory):
    """Memory for the Yeager agent."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #short term memory, last 10 interactions
        
        # entities memory, like variables in a conversation, paths, files, status, etc.of the current user and thread

        # load pinecone memory of the most similar interactions to the question of the current interaction of the same user and thread

        # load from shared infinite context memory pinecone most relevant interactions to the question topic with various formats
            # solution sketches
            # code snippets
            # api docs



