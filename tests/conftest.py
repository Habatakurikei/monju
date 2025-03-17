import json
import os
import sys
from pathlib import Path

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../monju"))


API_KEY_FILE = "api_key_pairs.txt"
TEST_OUTPUT_PATH = "test-outputs"


@pytest.fixture(scope="session", autouse=True)
def setup_api_client():
    pass


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--run-api",
        action="store_true",
        default=False,
        help="Run tests that make actual API calls"
    )
    parser.addoption(
        "--load-api-file",
        action="store_true",
        default=False,
        help="Load API keys from text file defined in conftest.py"
    )


def load_api_keys() -> str:
    return Path(API_KEY_FILE).read_text(encoding="utf-8")


def pack_parameters(**kwargs) -> dict:
    """
    Use this function to arrange entry parameters in dictionary format.
    """
    return kwargs


def save_as(filename: str, data: dict) -> None:
    """
    Save data to a file.
    """
    print(f"Result:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    os.makedirs(TEST_OUTPUT_PATH, exist_ok=True)
    with open(f"{TEST_OUTPUT_PATH}/{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
