import pytest

from conftest import load_api_keys
from conftest import pack_parameters
from conftest import save_as
from monju.config import DEFAULT_FREEDOM
from monju.config import DEFAULT_IDEAS
from monju.config import DEFAULT_LANGUAGE
from monju.config import KEY_CLASS_DIAGRAM
from monju.config import KEY_FREEDOM
from monju.config import KEY_IDEAS
from monju.config import KEY_IDEA_REDUCTION
from monju.config import KEY_INPUT
from monju.config import KEY_LANGUAGE
from monju.config import KEY_MINDMAP
from monju.config import KEY_THEME
from monju.monju import Monju


THEME = "How to survive in the era of emerging AI?"
IDEAS = 5
FREEDOM = 0.2
LANGUAGE = "en"


@pytest.fixture
def run_api(request) -> bool:
    return request.config.getoption("--run-api")


@pytest.fixture
def load_api_file(request) -> bool:
    return request.config.getoption("--load-api-file")


def test_monju_missing_theme() -> None:
    params = pack_parameters(ideas=IDEAS, freedom=FREEDOM, language=LANGUAGE)
    with pytest.raises(
        ValueError,
        match=f"{KEY_THEME} is not given or not str."
    ):
        Monju(**params)


def test_monju_missing_ideas() -> None:
    params = pack_parameters(theme=THEME, freedom=FREEDOM, language=LANGUAGE)
    monju = Monju(**params)
    assert monju.record[KEY_INPUT][KEY_IDEAS] == DEFAULT_IDEAS


def test_monju_missing_freedom() -> None:
    params = pack_parameters(theme=THEME, ideas=IDEAS, language=LANGUAGE)
    monju = Monju(**params)
    assert monju.record[KEY_INPUT][KEY_FREEDOM] == DEFAULT_FREEDOM


def test_monju_missing_language() -> None:
    params = pack_parameters(theme=THEME, ideas=IDEAS, freedom=FREEDOM)
    monju = Monju(**params)
    assert monju.record[KEY_INPUT][KEY_LANGUAGE] == DEFAULT_LANGUAGE


def test_monju_no_parameters() -> None:
    with pytest.raises(
        ValueError,
        match="No parameters are given."
    ):
        Monju()


def test_monju_no_theme() -> None:
    params = pack_parameters(theme='')
    with pytest.raises(
        ValueError,
        match=f"{KEY_THEME} is not given or not str."
    ):
        Monju(**params)


def test_monju_wrong_theme() -> None:
    params = pack_parameters(theme=1)
    with pytest.raises(
        ValueError,
        match=f"{KEY_THEME} is not given or not str."
    ):
        Monju(**params)


def test_monju_batch(run_api: bool, load_api_file: bool) -> None:
    """
    Execution of monju brainstorming in batch mode.
    """
    judgment = True
    api_keys = ''
    params = pack_parameters(theme=THEME)

    if load_api_file:
        api_keys = load_api_keys()

    bs = Monju(api_keys=api_keys, verbose=True, reduction=False, **params)

    try:
        if run_api:
            bs.brainstorm()
    except Exception as e:
        pytest.fail(f"Error: {e}")

    save_as("monju_batch.json", bs.record)

    assert judgment is True


def test_monju_step_by_step(run_api: bool, load_api_file: bool) -> None:
    """
    Execution of monju brainstorming in step-by-step mode.
    """
    judgment = True
    api_keys = ''
    params = pack_parameters(
        theme=THEME,
        ideas=18,
        freedom=0.9,
        language="ja"
    )

    if load_api_file:
        api_keys = load_api_keys()

    bs = Monju(api_keys=api_keys, verbose=True, reduction=False, **params)

    try:
        if run_api:
            print(f"Status: {bs.status}")
            bs.generate_ideas(**{
                "openai_ideation": {
                    "provider": "openai",
                    "model": "gpt-4.5-preview"
                },
                "anthropic_ideation": {
                    "provider": "anthropic",
                    "model": "claude-3-7-sonnet-latest"
                },
                "google_ideation": {
                    "provider": "google",
                    "model": "gemini-2.0-flash"
                }
            })

            print(f"Status: {bs.status}")
            bs.reduce_ideas()

            print(f"Status: {bs.status}")
            bs.organize_ideas(**{
                KEY_MINDMAP: {
                    "provider": "deepseek"
                },
                KEY_CLASS_DIAGRAM: {
                    "provider": "deepseek"
                }
            })

            print(f"Status: {bs.status}")
            bs.evaluate_ideas(**{
                "openai_evaluation": {
                    "provider": "openai",
                    "model": "gpt-4o-mini"
                },
                "anthropic_evaluation": {
                    "provider": "anthropic",
                    "model": "claude-3-haiku-20240307"
                },
                "google_evaluation": {
                    "provider": "google",
                    "model": "gemini-1.5-flash"
                }
            })

            print(f"Status: {bs.status}")
            bs.verify()

            print(f"Status: {bs.status}")

    except Exception as e:
        pytest.fail(f"Error: {e}")

    save_as("monju_sbs.json", bs.record)

    assert judgment is True


def test_monju_reasoning(run_api: bool, load_api_file: bool) -> None:
    """
    Execution of monju reasoning.
    """
    judgment = True
    api_keys = ''
    params = pack_parameters(
        theme=THEME,
        ideas=20,
        freedom=0.2,
        language="ja"
    )

    if load_api_file:
        api_keys = load_api_keys()

    bs = Monju(api_keys=api_keys, verbose=True, reduction=True, **params)

    try:
        if run_api:
            print(f"Status: {bs.status}")
            bs.generate_ideas()

            print(f"Status: {bs.status}")
            bs.reduce_ideas(**{
                KEY_IDEA_REDUCTION: {
                    "provider": "deepseek",
                    "temperature": 0.0
                }
            })

            print(f"Status: {bs.status}")
            bs.organize_ideas(**{
                KEY_MINDMAP: {
                    "provider": "deepseek",
                    "temperature": 0.0
                },
                KEY_CLASS_DIAGRAM: {
                    "provider": "deepseek",
                    "temperature": 0.0
                }
            })

            print(f"Status: {bs.status}")
            bs.evaluate_ideas(**{
                "openai": {
                    "provider": "openai",
                    "model": "o3-mini",
                    "reasoning_effort": "high"
                },
                "anthropic": {
                    "provider": "anthropic",
                    "model": "claude-3-7-sonnet-20250219",
                    "thinking": {"type": "enabled", "budget_tokens": 10000},
                    "max_tokens": 128000
                },
            })

            print(f"Status: {bs.status}")
            bs.verify()

            print(f"Status: {bs.status}")

    except Exception as e:
        pytest.fail(f"Error: {e}")

    save_as("monju_reasoning.json", bs.record)

    assert judgment is True
