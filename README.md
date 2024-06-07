# python-gpt-worldgen
WorldGen CLI tool - create a new events / periods / scenes (heavily inspired by Microscope RPG!!)

## Generated Examples

### Periods

```yaml
events: []
id: MMMM
overview: During The Nexus Convergence, various species and civilizations across the
  galaxies unite to form a network of interconnected minds, ushering in an era of
  unparalleled collaboration and shared consciousness.
title: The Nexus Convergence
```

### GPT Prompts

- [](templates/prompts/suggest_period.md)
- [](templates/prompts/start_brainstorm_story_ideas.jinja.md)
- [](https://github.com/david-wolgemuth/python-gpt-worldgen/blob/main/templates/prompts/suggest_genre.md)

### CLI

```sh
python main.py --help

python main.py period suggest ./builds/my_world/periods/CCCC-hello-world
> Suggested period: CCCC-hello-world: Dawn of Unity
> A period of profound transformation as disparate societies merge into unified superorganisms.
```

python

```py
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
```
