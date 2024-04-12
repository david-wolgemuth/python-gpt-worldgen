## Instructions

The user is building a fictional world

```yaml
title: {{ build.title }}
overview:  {{ build.overview }}
```

The have already defined the following periods,
and want a suggestion in the supplied location:

```yaml
{% for period in periods %}
{% if period.id == period_id %}
## SUGGEST FOR THIS PERIOD
{% endif %}
- id: {{ period.id }}
  title: {{ period.title }}
  overview: {{ period.overview }}
  events:
  {% for event in period.events %}
    - {{ event.title }}
  {% endfor %}
{% endfor %}
```

### Notes

- The title should be quick and straightforward
- The overview should be one or two sentences
- Generally should not introduce new concepts or characters, but expand on existing concepts and characters

### Format

Format as JSON

```json
{
    "title": "My Example Period",
    "overview": "My Example Overview"
}
```
