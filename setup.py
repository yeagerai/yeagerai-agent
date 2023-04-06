from setuptools import setup, find_packages

setup(
    name="yeager.ai-framework",
    version="0.0.2",
    description="A high-level Python framework for building complex LangChain agents on-the-fly just by prompting.",
    author="YeagerAI LLC",
    author_email="jm@yeager.ai",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "openai",
        "discord.py",
        "PyGithub",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: YeagerAI",
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