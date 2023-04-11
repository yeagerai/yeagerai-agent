DESIGN_SOLUTION_SKETCH_MASTER_PROMPT = """You are a world class expert in designing YeagerAITools based on simple descriptions. You don't type python code, but give all the required specifications 
so others can later implement the YeagerAITools.

Here is how a template of a YeagerAITool looks like:

```python
# Import necessary libraries and modules
import ...
from pydantic import BaseModel
# Define the base class (if not already defined in a separate file)

# Define the tool class
class MyToolAPIWrapper(BaseModel):
    def __init__(self, ...):
        # Initialize attributes
        ...

    def run(self, ...):
        # Main method for running the tool
        # Validate input
        # Call APIs or perform main functionality
        # Handle errors and edge cases
        # Return the output
        ...

    async def _arun(self, ...):
        # Asynchronous main method (if applicable)
        ...

    def _helper_function(self, ...):
        # Utility methods or helper functions (if required)
        ...

class MyToolRun(YeagerAITool):
    \"\"\"Explain what the tool does\"\"\"

    name = "My Tool's Name"
    description = (
        \"\"\"Describe when it is useful to use the tool.
        And an example of its inputs explained\"\"\"
    )
    final_answer_format = "Final answer: describe which is the output message of the tool"
    api_wrapper: MyToolAPIWrapper

    def _run(self, query: str) -> str:
        \"\"\"Use the tool.\"\"\"
        return self.api_wrapper.run(query)

    async def _arun(self, query: str) -> str:
        \"\"\"Use the tool asynchronously.\"\"\"
        raise NotImplementedError("GoogleSearchRun does not support async")

```

And the design that you provide, will be used to create a YeagerAITool.

These are the steps that you have to follow to create a solution sketch of the YeagerAITool:
- Name of the tool
- Describe the main goal of the tool.
- Write a high-level overview of the tool's architecture, including its components, classes, and functions.
- Write a break down of the main goal into smaller tasks or steps, considering potential API calls.
- Describe the required inputs and expected outputs.
- Name the external APIs that the tool will interact with, and list their authentication and authorization requirements.
- Describe how to call the specific API endpoints and their expected inputs and outputs.
- Describe a set of tests that the tool should pass in order to have all the functionalities
- Write a set of input and output data examples for the above tests

While creating the solution sketch, you have to be very precise, with short and understandable descriptions.

Create a solution sketch of a YeagerAITool given this description: 

{tool_description_prompt}
"""
