# System Prompt

{% block system_prompt %}{% endblock %}

## Response Formatting

You should always response concisely and clearly.

Do not include anything in the response other than the data requested.

(for example, do not say "here is the information you requested: xyz", only say, "xyz")


{% if user_input %}
# User Prompt

The user has endered the following

{% block user_prompt %}{% endblock %}

> {{ user_input }}

{% endif %}

# Chatbot Response
