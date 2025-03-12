import json
import re


def sanitize_mermaid(source: str) -> str:
    """
    Sanitize mermaid text to avoid errors.
    Strip markdown syntax and replace some characters for Japanese.
    """
    pattern = r"^\s*```(\w+)\n(.*?)\n\s*```"
    match = re.match(pattern, source, re.DOTALL | re.MULTILINE)
    text = match[2]
    # text = text.replace("&", "and")
    text = text.replace("・", "-")
    text = text.replace("(", "-")
    text = text.replace(")", "-")
    return text


def remove_highlight(source: str) -> str:
    """
    Remove highlight syntax in evaluation text.
    """
    return source.replace("**", "").replace("#", "")


def print_record(record: dict) -> None:
    """
    Print record in a readable format.
    """
    record_str = json.dumps(record, indent=2, ensure_ascii=False)
    print(f"Record:\n{record_str}")
