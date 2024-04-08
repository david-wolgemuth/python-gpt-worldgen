{% extends "prompts/base.md" %}
{% block system_prompt %}

### Literature Genres and Subgenres Request

Dear AI,

List genres and subgenres. Structure the response by main genre, followed by its subgenres.

Example Output:

```yaml
- Fantasy:
  - High Fantasy
  - Urban Fantasy
  - Dark Fantasy
- Science Fiction:
  - Hard Sci-Fi
  - Space Opera
  - Cyberpunk
- Mystery:
  - Cozy Mystery
  - Police Procedural
  - Noir
```

{% endblock %}
{% block user_prompt %}

The user specifically requested genres related to the following:

{% endblock %}
