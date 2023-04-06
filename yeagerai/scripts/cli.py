import os
import click

from dotenv import load_dotenv

from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain.llms import OpenAI

from yeagerai.y_kits_lib.tool_creation_kit.tool_creation_kit import tckit

# from yeagerai.agents.yeager_base_agent import YeagerBaseAgent
# agent = YeagerBaseAgent()
# agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tool_creation_toolkit, verbose=True)

load_dotenv()

llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
agent_executor = initialize_agent(
    tools=tckit.tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)


def yAgentBuilder(prompt_text):
    agent_executor.run(prompt_text)


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
    type=click.Choice(["yagentbuilder"]),
    help="Select the agent you want to use.",
)
def main(agent):
    click.echo(
        click.style("Welcome to the Yeager.ai Framework!\n", fg="green", bold=True)
    )

    if agent == "yagentbuilder":
        click.echo(click.style("Entering yAgentBuilder chat interface...", fg="green"))
        chat_interface(yAgentBuilder)
    else:
        click.echo(
            "Please provide a valid agent using the --agent option. For help, use --help."
        )


if __name__ == "__main__":
    main()
