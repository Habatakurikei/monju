import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../monju'))

import pytest

from monju.config import DEFAULT_FREEDOM
from monju.config import DEFAULT_IDEAS
from monju.config import DEFAULT_LANGUAGE
from monju.config import KEY_FREEDOM
from monju.config import KEY_IDEAS
from monju.config import KEY_INPUT
from monju.config import KEY_LANGUAGE
from monju.config import KEY_THEME
from monju import Monju


# API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
API_KEY = ''

THEME = 'How to survive in the era of emerging AI?'
IDEAS = 5
FREEDOM = 0.2
LANGUAGE = 'en'

OUTPUT_DIR = Path('test-output')


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def pack_parameters(**kwargs):
    '''
    Use this function to arrange entry parameters in dictionary format.
    '''
    return kwargs


def test_monju_missing_theme():
    params = pack_parameters(ideas=IDEAS, freedom=FREEDOM, language=LANGUAGE)
    with pytest.raises(ValueError,
                       match=f'{KEY_THEME} is not given or not str.'):
        Monju(api_keys=API_KEY, **params)


def test_monju_missing_ideas():
    params = pack_parameters(theme=THEME, freedom=FREEDOM, language=LANGUAGE)
    monju = Monju(api_keys=API_KEY, **params)
    assert monju.record[KEY_INPUT][KEY_IDEAS] == DEFAULT_IDEAS


def test_monju_missing_freedom():
    params = pack_parameters(theme=THEME, ideas=IDEAS, language=LANGUAGE)
    monju = Monju(api_keys=API_KEY, **params)
    assert monju.record[KEY_INPUT][KEY_FREEDOM] == DEFAULT_FREEDOM


def test_monju_missing_language():
    params = pack_parameters(theme=THEME, ideas=IDEAS, freedom=FREEDOM)
    monju = Monju(api_keys=API_KEY, **params)
    assert monju.record[KEY_INPUT][KEY_LANGUAGE] == DEFAULT_LANGUAGE


def test_monju_no_parameters():
    with pytest.raises(ValueError,
                       match='No parameters are given.'):
        Monju()


def test_monju_no_theme():
    params = pack_parameters(theme='')
    with pytest.raises(ValueError,
                       match=f'{KEY_THEME} is not given or not str.'):
        Monju(api_keys=API_KEY, **params)


def test_monju_batch(run_api):

    judgment = True

    params = pack_parameters(theme=THEME,
                             ideas=IDEAS,
                             freedom=FREEDOM,
                             language=LANGUAGE)
    bs = Monju(api_keys=API_KEY, verbose=True, **params)

    try:
        if run_api:
            bs.brainstorm()
    except Exception as e:
        pytest.fail(f'Error: {e}')

    print(f'Result:\n{json.dumps(bs.record, indent=2, ensure_ascii=False)}')

    save_as = OUTPUT_DIR / 'monju_batch.json'
    with open(save_as, 'w', encoding='utf-8') as f:
        json.dump(bs.record, f, indent=2, ensure_ascii=False)

    assert judgment is True


def test_monju_step_by_step(run_api):

    judgment = True

    params = pack_parameters(theme=THEME,
                             ideas=3,
                             freedom=0.8,
                             language='ja')
    bs = Monju(api_keys=API_KEY, verbose=True, **params)

    try:
        if run_api:

            print(f"Status: {bs.status}")
            bs.generate_ideas(**{
                'openai_ideation': {
                    'provider': 'openai',
                    'model': 'gpt-4o-mini'
                },
                'anthropic_ideation': {
                    'provider': 'anthropic',
                    'model': 'claude-3-haiku-20240307'
                },
                'google_ideation': {
                    'provider': 'google',
                    'model': 'gemini-1.5-flash'
                }
            })

            print(f"Status: {bs.status}")
            bs.organize_ideas(**{
                'claude_organization': {
                    'provider': 'anthropic',
                    'model': 'claude-3-5-sonnet-20241022'
                }
            })

            print(f"Status: {bs.status}")
            bs.evaluate_ideas(**{
                'openai_evaluation': {
                    'provider': 'openai',
                    'model': 'gpt-4o-mini'
                },
                'anthropic_evaluation': {
                    'provider': 'anthropic',
                    'model': 'claude-3-haiku-20240307'
                },
                'google_evaluation': {
                    'provider': 'google',
                    'model': 'gemini-1.5-flash'
                }
            })

            print(f"Status: {bs.status}")
            bs.verify()

            print(f"Status: {bs.status}")

    except Exception as e:
        pytest.fail(f'Error: {e}')

    print(f'Result:\n{json.dumps(bs.record, indent=2, ensure_ascii=False)}')

    save_as = OUTPUT_DIR / 'monju_sbs.json'
    with open(save_as, 'w', encoding='utf-8') as f:
        json.dump(bs.record, f, indent=2, ensure_ascii=False)

    assert judgment is True
