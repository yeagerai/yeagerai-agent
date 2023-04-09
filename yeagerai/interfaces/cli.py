import os

import click
import getpass
import uuid

from dotenv import load_dotenv

from yeagerai.agent import YeagerAIAgent

def chat_interface():
    while True:
        try:
            prompt_text = input("\n\nEnter your prompt (Type :q to quit):\n\n> ")
            if prompt_text == ":q":
                break

            y_agent_builder.run(prompt_text)

        except KeyboardInterrupt:
            continue
        except EOFError:
            break


@click.command()
def main():
    click.echo(
        click.style("Welcome to the @yeager.ai CLI!\n", fg="green", bold=True)
    )

    click.echo(click.style("Loading The @yeager.ai Agent Interface...", fg="green"))
    chat_interface()


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
    load_dotenv()

    username, session_id, session_path = create_or_restore_session()

    y_agent_builder = YeagerAIAgent(
        username=username,
        session_id=session_id,
        session_path=session_path,
    )

    # start conversation
    main()
