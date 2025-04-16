# Constants

DEFAULT_FREEDOM = 0.7
DEFAULT_IDEAS = 10
DEFAULT_LANGUAGE = "en"
DEFAULT_TEMPERATURE_CLASS_DIAGRAM = 0.0
DEFAULT_TEMPERATURE_EVALUATION = 0.7
DEFAULT_TEMPERATURE_MINDMAP = 0.0
DEFAULT_TEMPERATURE_IDEA_GENERATION = 0.0
KEY_CLASS_DIAGRAM = "class_diagram"
KEY_ELAPSED_TIME = "elapsed_time"
KEY_EVALUATION = "evaluation"
KEY_FREEDOM = "freedom"
KEY_IDEA_LIST = "idea_list"
KEY_IDEA_REDUCTION = "idea_reduction"
KEY_IDEAS = "ideas"
KEY_INPUT = "input"
KEY_LANGUAGE = "language"
KEY_MINDMAP = "mindmap"
KEY_OUTPUT = "output"
KEY_THEME = "theme"
PROGRESS_DONE = "done"
PROGRESS_FAILED = "failed"
PROGRESS_IDEA_EVALUATION = "idea_evaluation"
PROGRESS_IDEA_GENERATION = "idea_generation"
PROGRESS_NOT_STARTED = "not_started"
PROGRESS_ORGANIZING = "organizing"
PROGRESS_REDUCING = "reducing"
PROGRESS_VERIFYING = "verifying"
WAIT_FOR_STARTING = 0.1

# Candidate LLM Models

KEY_ANTHROPIC = "anthropic"
KEY_GOOGLE = "google"
KEY_OPENAI = "openai"

LLM_IDEA_GENERATION = {
    KEY_OPENAI: {
        "provider": KEY_OPENAI,
        "model": "gpt-4.1-nano",
    },
    KEY_ANTHROPIC: {
        "provider": KEY_ANTHROPIC,
        "model": "claude-3-haiku-20240307",
    },
    KEY_GOOGLE: {
        "provider": KEY_GOOGLE,
        "model": "gemini-1.5-flash",
    },
}

LLM_IDEA_REDUCTION = {
    KEY_IDEA_REDUCTION: {
        "provider": KEY_GOOGLE,
        "model": "gemini-2.0-flash",
    }
}

LLM_IDEA_ORGANIZATION = {
    KEY_MINDMAP: {
        "provider": KEY_OPENAI,
        "model": "gpt-4o",
    },
    KEY_CLASS_DIAGRAM: {
        "provider": KEY_OPENAI,
        "model": "gpt-4o",
    },
}

LLM_IDEA_EVALUATION = {
    KEY_OPENAI: {
        "provider": KEY_OPENAI,
        "model": "gpt-4.1-nano",
    },
    KEY_ANTHROPIC: {
        "provider": KEY_ANTHROPIC,
        "model": "claude-3-haiku-20240307",
    },
    KEY_GOOGLE: {
        "provider": KEY_GOOGLE,
        "model": "gemini-2.0-flash",
    },
}

# Prompts

IDEA_GENERATION_PROMPT = '''
Purpose: Generate $ideas ideas on the following "Theme" and meeting the "Conditions".

Conditions:
1. Propose ideas with free thinking.
2. Return the results in bullet points as shown in the "Format".
3. The language of the output is in $language of ISO 639-1 format.
4. Do not include your explanations.
5. Do not add any unnecessary decorations to the bullet points.

Theme: $theme

Format:
- Idea
'''

IDEA_REDUCTION_PROMPT = '''
Purpose: Remove duplicate ideas from the "Idea List".

Conditions:
1. The language of the output is in $language of ISO 639-1 format.
2. Return the results also in the same list format.
3. Do not include your explanations.
4. Do not add any unnecessary decorations to the bullet points.

Idea List:
$idea_list
'''

MINDMAP_GENERATION_PROMPT = '''
Purpose: Organize the "Idea List" into a mindmap based on the "Theme" and meeting the "Conditions".

Theme: $theme

Conditions:
1. Output the result in "Format" as Mermaid chart. Do not include your explanations.
2. Group similar items in the "Idea List" into several groups and create a hierarchical structure.
3. The language of the output is in $language of ISO 639-1 format.

Idea List:
$idea_list

Format:
```mermaid
mindmap
    $theme
        (Summary of ideas)
            (Idea item)
```
'''

CLASS_DIAGRAM_GENERATION_PROMPT = '''
Purpose: Organize the "Idea List" into a class diagram based on the "Theme" and meeting the "Conditions".

Theme: $theme

Conditions:
1. Output the result in "Format" as Mermaid chart. Do not include your explanations.
2. Make 3 to 7 groups by finding similar items in the "Idea List",  and define `class` for output.
3. Look for classes that seem related and draw line between them using `-->` for output.
4. The language of the output is in $language of ISO 639-1 format.

Idea List:
$idea_list

Format:
```mermaid
classDiagram
    class ClassA {
        idea
    }
    class ClassB {
        idea
    }
    ClassA --> ClassB
```
'''

EVALUATION_PROMPT = '''
Purpose: Evaluate the "Mindmap" based on the "Theme" and meeting the "Conditions".

Theme: $theme

Conditions:
1. Write "Overall Evaluation", "Good Points", and "Areas for Improvement" according to the "Format".
2. Write as concisely and focused on key points as possible.
3. The language of the output is in $language of ISO 639-1 format.
4. Do not add any unnecessary decorations to the bullet points.

Mindmap:
$mermaid_mindmap

Format:
- Overall Evaluation:
  - Bullet point
- Good Points:
  - Bullet point
- Areas for Improvement:
  - Bullet point
'''
