import os

import click
import getpass
import uuid

from dotenv import load_dotenv

from yeagerai.core.y_kit import YeagerKit
from yeagerai.agents.y_agent_builder.kit.create_tool_source.create_tool_source import (
    CreateToolSourceRun,
    CreateToolSourceAPIWrapper,
)
from yeagerai.core.y_memory import YeagerContextMemory
from yeagerai.core.y_base_agent import YeagerBaseAgent
from yeagerai.callbacks.curate_n_store_memory import MemoryCallbackHandler
from yeagerai.callbacks.git_local_repo import GitLocalRepoCallbackHandler


def yAgentBuilder(prompt_text):
    y_agent_builder.run(prompt_text)


def chat_interface(selected_function):
    while True:
        try:
            prompt_text = input("\n\nEnter your prompt (Type :q to quit):\n\n> ")
            if prompt_text == ":q":
                break

            selected_function(prompt_text)

        except KeyboardInterrupt:
            continue
        except EOFError:
            break


@click.command()
@click.option(
    "--agent",
    type=click.Choice(["yAgentBuilder"]),
    help="Select the agent you want to use.",
)
def main(agent):
    click.echo(
        click.style("Welcome to the Yeager.ai Framework!\n", fg="green", bold=True)
    )

    if agent == "yAgentBuilder":
        click.echo(click.style("Entering yAgentBuilder chat interface...", fg="green"))
        chat_interface(yAgentBuilder)
    else:
        click.echo(
            "Please provide a valid agent using the --agent option. For help, use --help."
        )


def create_or_restore_session():
    username = getpass.getuser()
    previous_session_id = input(
        "Enter the session_id of an already existing session to continue working with it (leave empty if you want to start a new session): "
    )
    if previous_session_id:
        session_id = previous_session_id
        home_path = os.path.expanduser("~")
        session_path = os.path.join(home_path, "yeagerai-sessions", session_id)
        if os.path.exists(session_path):
            print(f"Session {session_id} already exists. Continuing with it.")
        else:
            print(f"Session {session_id} does not exist. Creating a new session.")
            session_id = str(uuid.uuid1()) + "-" + username
            home_path = os.path.expanduser("~")
            session_path = os.path.join(home_path, "yeagerai-sessions", session_id)
    else:
        session_id = str(uuid.uuid1()) + "-" + username
        home_path = os.path.expanduser("~")
        session_path = os.path.join(home_path, "yeagerai-sessions", session_id)

    return username, session_id, session_path


if __name__ == "__main__":
    # load the .env file
    load_dotenv()

    # start or continue with the session
    username, session_id, session_path = create_or_restore_session()

    # instantiate the local repo callback
    git_repo_callback = GitLocalRepoCallbackHandler(
        username=username, session_path=session_path
    )

    memory = YeagerContextMemory(username, session_id, session_path)

    curate_memory = MemoryCallbackHandler(
        username=username, session_path=session_path, context_memory=memory
    )

    # instantiate the YeagerKit
    tckit = YeagerKit()
    tckit.register_tool(
        CreateToolSourceRun(
            api_wrapper=CreateToolSourceAPIWrapper(session_path=session_path)
        )
    )

    # instantiate the agent
    y_agent_builder = YeagerBaseAgent(
        name="yAgentBuilder",
        description="A Yeager.ai agent that uses Yeager.ai's agent creation kit to create custom LangChain agents from prompts.",
        preffix_template="",
        suffix_template="",
        openai_model_name="gpt-4",
        yeager_kit=tckit,
        memory=memory,
        callbacks=[curate_memory, git_repo_callback],
    )

    # start conversation
    main()
