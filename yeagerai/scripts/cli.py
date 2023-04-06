import click

from dotenv import load_dotenv

from yeagerai.agents.y_agent_builder import y_agent_builder

load_dotenv()


def yAgentBuilder(prompt_text):
    y_agent_builder.run(prompt_text)


# Newly created Agent calls
# for agents in created_agents_folder instantiate agent and create a new agent_executor with the corresponding tools


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


if __name__ == "__main__":
    main()
