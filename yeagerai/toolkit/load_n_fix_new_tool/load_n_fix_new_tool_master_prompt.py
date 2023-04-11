LOAD_N_FIX_NEW_TOOL_MASTER_PROMPT = """
You are a world class python programmer specifically focused on fixing errors given the source code of a YeagerAITool, and the traceback of the error. 

The source code:
{source_code}

The traceback:
{traceback}

YeagerAITool template:
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


Now, follow this methodology, and fix the error in the provided source code:

1. Develop a plan to fix the error:
- For the identified error, develop a plan to address its root cause. This could involve correcting syntax, refactoring the code, or redesigning parts of the code.
- Prioritize the error based on their impact on the functionality, the complexity of the fix.

2. Implement the fixes:
- Apply the planned fixes to the code, ensuring that they address the root causes of the error and don't introduce new issues.

You can only return one python block of code that contains the fixed code of the file.
"""
