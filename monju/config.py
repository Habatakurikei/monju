# Constants

DEFAULT_FREEDOM = 0.7
DEFAULT_IDEAS = 10
DEFAULT_LANGUAGE = 'EN'
DEFAULT_TEMPERATURE_CLASS_DIAGRAM = 0.0
DEFAULT_TEMPERATURE_EVALUATION = 0.7
DEFAULT_TEMPERATURE_MINDMAP = 0.0
KEY_CLASS_DIAGRAM = 'class_diagram'
KEY_ELAPSED_TIME = 'elapsed_time'
KEY_EVALUATION = 'evaluation'
KEY_FREEDOM = 'freedom'
KEY_IDEAS = 'ideas'
KEY_INPUT = 'input'
KEY_LANGUAGE = 'language'
KEY_MINDMAP = 'mindmap'
KEY_OUTPUT = 'output'
KEY_THEME = 'theme'
PROGRESS_DONE = 'done'
PROGRESS_FAILED = 'failed'
PROGRESS_IDEA_EVALUATION = 'idea_evaluation'
PROGRESS_IDEA_GENERATION = 'idea_generation'
PROGRESS_NOT_STARTED = 'not_started'
PROGRESS_ORGANIZING = 'organizing'
PROGRESS_VERIFYING = 'verifying'

# Candidate LLM Models
# - openai: gpt-4o-mini, gpt-4o-2024-08-06
# - anthropic: claude-3-haiku-20240307, claude-3-5-sonnet-20240620
# - google: gemini-1.5-flash, gemini-1.5-flash-exp-0827

KEY_ANTHROPIC = 'anthropic'
KEY_GOOGLE = 'google'
KEY_OPENAI = 'openai'

LLM_IDEA_GENERATION = {
    KEY_OPENAI: {
        'provider': KEY_OPENAI,
        'model': 'gpt-4o-mini'
    },
    KEY_ANTHROPIC: {
        'provider': KEY_ANTHROPIC,
        'model': 'claude-3-haiku-20240307'
    },
    KEY_GOOGLE: {
        'provider': KEY_GOOGLE,
        'model': 'gemini-1.5-flash'
    }
}

LLM_MINDMAP = {
    'provider': KEY_OPENAI,
    'model': 'gpt-4o'
}

LLM_CLASS_DIAGRAM = {
    'provider': KEY_OPENAI,
    'model': 'gpt-4o'
}

LLM_IDEA_EVALUATION = {
    KEY_OPENAI: {
        'provider': KEY_OPENAI,
        'model': 'gpt-4o-mini'
    },
    KEY_ANTHROPIC: {
        'provider': KEY_ANTHROPIC,
        'model': 'claude-3-haiku-20240307'
    },
    KEY_GOOGLE: {
        'provider': KEY_GOOGLE,
        'model': 'gemini-1.5-flash'
    }
}

# Prompts

IDEA_GENERATION_PROMPT = '''
Purpose: Generate {ideas} ideas on the following "Theme" and meeting the "Conditions".

Conditions:
1. Propose ideas with free thinking.
2. Consider the 5W1H when proposing.
3. Return the results in bullet points as shown in the "Format".
4. The language of the output is in {language} of ISO 639-1 format.
5. Do not include your explanations.
6. Do not add any unnecessary decorations to the bullet points.

Theme: {theme}

Format:
- Idea
'''

MINDMAP_GENERATION_PROMPT = '''
Purpose: Organize the "Idea List" into a mindmap based on the "Theme" and meeting the "Conditions".

Theme: {theme}

Conditions:
1. Group similar items in the "Idea List" into several groups and create a hierarchical structure.
2. Output the result in "Format" as Mermaid chart. Do not include your explanations.
3. The language of the output is in {language} of ISO 639-1 format.
4. Write the "Theme" as the root.
5. Enclose each idea item in parentheses () with an appropriate indent.

Idea List:
{idea_list}

Format:
```mermaid
mindmap
    root [Write the theme here]
        (Summary of ideas)
            (Idea item)
```
'''

CLASS_DIAGRAM_GENERATION_PROMPT = '''
Purpose: Organize the "Idea List" into a class diagram based on the "Theme" and meeting the "Conditions".

Theme: {theme}

Conditions:
1. Group similar items in the "Idea List" into several groups and make them classes.
2. Output the result in "Format" as Mermaid chart. Do not include your explanations.
3. The language of the output is in {language} of ISO 639-1 format.
4. Find the relationships between each class and reflect them in the class diagram.

Idea List:
{idea_list}

Format:
```mermaid
classDiagram
```
'''

EVALUATION_PROMPT = '''
Purpose: Evaluate the "Mindmap" based on the "Theme" and meeting the "Conditions".

Theme: {theme}

Conditions:
1. Write "Overall Evaluation", "Good Points", and "Areas for Improvement" according to the "Format".
2. The language of the output is in {language} of ISO 639-1 format.
3. Write as concisely and focused on key points as possible.
4. The mindmap is provided as a class diagram.
5. Do not add any unnecessary decorations to the bullet points.

Mindmap:
{mermaid_class}

Format:
- Overall Evaluation:
  - Bullet point
- Good Points:
  - Bullet point
- Areas for Improvement:
  - Bullet point
'''
