#!/usr/bin/env python3

import click
from jinja2 import Environment, FileSystemLoader, select_autoescape
from gpt4all import GPT4All
from time import sleep
from openai import OpenAI


import loaders
import models

# import signal

# This is our shared variable that indicates whether an interruption has been requested.
# interrupt_requested = False

# def signal_handler(signum, frame):
#     global interrupt_requested
#     interrupt_requested = True

# # Register the signal handler for SIGINT (Ctrl+C)
# signal.signal(signal.SIGINT, signal_handler)


templates = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['md'])
)


# def get_model():
#     return GPT4All("mistral-7b-openorca.gguf2.Q4_0.gguf")


def chat_completion(
    system_prompt: str,
    user_prompt: str,
) -> str:
    """
    https://platform.openai.com/docs/api-reference/chat/create
    """
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return completion.choices[0].message.content


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


@period.command(
    name="list",
    help="List periods."
)
@click.argument(
    "build_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
)
def list_periods(build_path):
    """List periods."""
    # for all `overview.md` files in the `periods` directory of the provided "build" path
    build = loaders.load_build(build_path)
    for period in build.periods:
        print(f"- {period.id}: {period.title}")


import os
import yaml
import dataclasses


@period.command(
    name="create",
    help="Create a period."
)
@click.argument(
    "build_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
)
@click.argument(
    "period_id",
    type=click.STRING,
    required=True,
)
def create_period(build_path, period_id):
    """Create a period."""
    # create a new period directory in the `periods` directory of the provided "build" path
    blank_period = models.Period(
        id=period_id,
        title="",
        overview="",
        events=[],
    )

    with open(os.path.join(build_path, "periods", period_id, "period.yaml"), "w") as f:
        yaml.dump(dataclasses.asdict(blank_period), f)

    # create empty `events` directory in the new period directory
    os.makedirs(os.path.join(build_path, "periods", period_id, "events"))


@period.command(
    name="show",
    help="Show a period."
)
@click.argument(
    "period_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
)
def show_period(period_path):
    """Show a period."""
    period = loaders.load_period(period_path)
    print(f"{period.id}: {period.title}")
    print(period.overview)
    for event in period.events:
        print(f"  - {event.id}: {event.title}")


@cli.group(invoke_without_command=True)
@click.pass_context
def event(ctx):
    """Define an event."""
    if ctx.invoked_subcommand is None:
        click.echo(event.get_help(ctx))


@event.command(
    name="create",
    help="Create an event."
)
@click.argument(
    "period_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
)
@click.argument(
    "event_id",
    type=click.STRING,
    required=True,
)
def create_event(period_path, event_id):
    """Create an event."""
    # create a new event directory in the `events` directory of the provided "period" path
    blank_event = models.Event(
        id=event_id,
        title="",
        overview="",
    )

    with open(os.path.join(period_path, "events", event_id, "event.yaml"), "w") as f:
        yaml.dump(dataclasses.asdict(blank_event), f)


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
