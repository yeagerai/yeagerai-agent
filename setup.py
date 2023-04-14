from setuptools import setup, find_packages

setup(
    name="yeagerai-agent",
    version="0.0.39",
    description="The @yeagerai Agent is used to create your custom LangChain Agents on-the-fly.",
    author="YeagerAI LLC",
    author_email="jm@yeager.ai",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "chromadb",
        "openai",
        "GitPython",
        "click",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "yeagerai-agent = yeagerai.interfaces.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
