#from langchain.llms.base import BaseLLM
import langchain.llms

llm_classes = {cls.__name__: cls for cls in langchain.llms.__dict__.values()
                if isinstance(cls, type) and issubclass(cls, langchain.llms.BaseLLM)}

llm_defaults = {
    "ChatOpenAI": {

    },
    "GPT4All": {
        "model":"./models/ggml-gpt4all-j.bin", 
        "n_ctx":512, 
        "n_threads":8
    }
}

def SimpleLLMFactory(llm_type: str, **kwargs) -> langchain.llms.BaseLLM:
    """Returns a new instance of any BaseLLM available 
    in 'import langchain.llms'

    Args:
        llm_type (str): The type of llm you want

    Raises:
        ValueError: Type was not found. Check spelling

    Returns:
        BaseLLM: Instanciated with the **kwargs provided
    """
    
    global llm_classes 
    global llm_defaults
    try:
        return llm_classes[llm_type](**{**llm_defaults.get(llm_type,{}), **kwargs})
    except KeyError:
        raise ValueError(f"Unknown LLM type: {llm_type}")