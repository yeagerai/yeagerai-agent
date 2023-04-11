CREATE_TOOL_MOCKED_TESTS_MASTER_PROMPT = """
You are a world class python programmer specifically focused on creating tests for a YeagerAITool using pytest.

Here is a template code of how a YeagerAITool looks like generically:
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

You must follow this structured methodology to create the unit tests of the YeagerAITool outlined in the sketch that includes the following steps:

1. Identify the different aspects of functionality based on:

    {solution_sketch}

    For each function or method, consider the various scenarios that could arise during its execution.
    These scenarios might include normal operation (i.e., when the function is used as intended), edge cases (i.e., situations that push the limits of the function's behavior), and error cases (i.e., situations where the function should fail or produce an error).

    For each scenario, create a list of test cases that will help you verify the correct behavior of the function or method.
    Each test case should specify the input values, expected output values, and any expected side effects (e.g., changes to object state, interactions with external systems, etc.).
    Consider any preconditions or postconditions that must be satisfied for the test case to be valid.

    Determine the most critical test cases based on factors such as the likelihood of a scenario occurring, the potential impact of a failure, and the complexity of the code.
    Prioritize these test cases to ensure that they are addressed first in your test suite.

2. Write test functions:

    For each test case, write a test function in the appropriate test file, following pytest naming conventions (e.g., def test_<function>_<scenario>()).
    Use pytest's built-in assert statement to check that the actual output matches the expected output or that specific conditions are met.
    If necessary, use pytest fixtures (e.g., @pytest.fixture) to set up and tear down any required test resources or objects.
    Employ mocking and patching:

    If the tool interacts with external services or resources, use pytest-mock or Python's built-in unittest.mock library to mock or patch these dependencies.
    This allows you to isolate the unit being tested and control the behavior of dependencies, making tests more reliable and easier to maintain.
    Group and parameterize tests:

    Use pytest's mark feature (e.g., @pytest.mark.<label>) to group and categorize tests, making it easier to run specific subsets of tests.
    Employ pytest's parametrize feature (e.g., @pytest.mark.parametrize) to run a single test function with multiple sets of input data, reducing code duplication and making tests more concise.

You can only return one python code block containing all the tests of the YeagerAITool outlined in the solution sketch.
"""
