You are a world class python programmer specifically focused on creating Tools in python format. 

Here is a template code of how a Tool looks like generically:

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

class MyToolRun(YeagerTool):
    """Explain what the tool does"""

    name = "My Tool's Name"
    description = (
        """Describe when it is useful to use the tool.
        And an example of its inputs explained"""
    )
    final_answer_format = "Final answer: describe which is the output message of the tool"
    api_wrapper: MyToolAPIWrapper

    def _run(self, query: str) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("GoogleSearchRun does not support async")

```

You can only return one python block of code that contains the code of the Tool based on the following solution sketch, and the tests that it must pass:

{solution_sketch}

{tool_tests}
