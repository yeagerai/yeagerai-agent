import click

def yAgentBuilder(prompt_text):
    # Add your agent.run() logic here
    out = f"yAgentBuilder: {prompt_text}"
    return out

def yTools(prompt_text):
    # Add your agent.run() logic here
    out = f"yTools: {prompt_text}"
    return out

def chat_interface(selected_function):
    while True:
        try:
            prompt_text = input("Enter your prompt (Type :q to quit): ")
            if prompt_text == ":q":
                break

            out = selected_function(prompt_text)
            click.echo(f"Output: {out}")

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

@click.command()
@click.option("--agent", type=click.Choice(["yagentbuilder", "ytools"]), help="Select the agent you want to use.")
def main(agent):
    click.echo(click.style("Welcome to the Yeager.ai Framework!\n", fg="green", bold=True))

    if agent == "yagentbuilder":
        click.echo(click.style("Entering yAgentBuilder chat interface...", fg="green"))
        chat_interface(yAgentBuilder)
    elif agent == "ytools":
        click.echo(click.style("Entering yTools chat interface...", fg="green"))
        chat_interface(yTools)
    else:
        click.echo("Please provide a valid agent using the --agent option. For help, use --help.")

if __name__ == "__main__":
    main()
