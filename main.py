#!/usr/bin/env python3

import click
from jinja2 import Environment, FileSystemLoader, select_autoescape
from gpt4all import GPT4All
from time import sleep

import signal

# This is our shared variable that indicates whether an interruption has been requested.
interrupt_requested = False

def signal_handler(signum, frame):
    global interrupt_requested
    interrupt_requested = True

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)


templates = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['md'])
)


def get_model():
    return GPT4All("mistral-7b-openorca.gguf2.Q4_0.gguf")


# Utilize asyncio to control the pace of character streaming
def stream_characters(text, delay=0.01):
    """Stream characters to the terminal, one at a time."""
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)


def stream_response(token_id, token_string):
    """Stream the response from the model."""
    global interrupt_requested
    if interrupt_requested:
        print("\nInterruption requested, terminating callback.")
        return False

    stream_characters(token_string)
    return True

# Define click group for organizing commands
@click.group()
def cli():
    """WorldGen CLI tool for generating events, scenes, and periods."""
    pass


# Command for generating an event
@cli.command()
def event():
    """Generate an event."""
    stream_characters("Generating an event...")


# Command for creating a scene
@cli.command()
def scene():
    """Create a scene."""
    stream_characters("Creating a scene...")


# Command for defining a period
@cli.group(invoke_without_command=True)
@click.pass_context
def period(ctx):
    """Define a period."""
    if ctx.invoked_subcommand is None:
        click.echo(period.get_help(ctx))


# Subcommand for listing periods
@period.command(
    name="suggest",
    help="Suggest period for inspiration."
)
def suggest_period():
    """Suggest a period"""
    model = get_model()

    with model.chat_session():
        prompt = templates.get_template("prompts/suggest_period.md").render()

        model.generate(
            prompt,
            temp=1.4,
            max_tokens=400,
            callback=stream_response,
            repeat_penalty=1.6,
        )


@cli.group(invoke_without_command=True)
@click.pass_context
def genre(ctx):
    """
    Pick a genre for the story.
    
    This should be done at the beginning of the story generation process, and not after.
    """
    if ctx.invoked_subcommand is None:
        click.echo(genre.get_help(ctx))

    
@genre.command(
    name="suggest",
    help="Suggest various genres for inspiration."
)
@click.option(
    "-p",
    "--parent_genre",
    help="""Will suggest sub-genres under the provided genre.""",
)
def suggest_genres(parent_genre=None):
    """Generate list for the story."""
    model = get_model()
    with model.chat_session():
        prompt = templates.get_template("prompts/suggest_genres.md").render({
            "parent_genre": parent_genre,
        })

        model.generate(
            prompt,
            temp=1.4,
            max_tokens=400,
            callback=stream_response,
            repeat_penalty=1.6,
        )


@genre.command(
    name="set",
    help="Set the genre for the story."
)
@click.argument(
    "genre",
    type=click.STRING,
    required=True,
)
def set_genre(genre):
    """Set the genre for the story."""
    pass


@cli.command()
def start():
    """Start the WorldGen CLI tool."""

    welcome_message = templates.get_template("start.md").render()
    stream_characters(welcome_message)


if __name__ == '__main__':
    cli()
