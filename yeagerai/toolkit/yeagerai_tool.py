from langchain.tools import BaseTool


class YeagerTool(BaseTool):
    final_answer_format: str
