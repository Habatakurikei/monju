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
LANGUAGE = 'EN'


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
        Monju(api_keys=API_KEY)


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

    print(f'Result:\n{json.dumps(bs.record, indent=2)}')

    with open('monju_batch.json', 'w', encoding='utf-8') as f:
        json.dump(bs.record, f, indent=2, ensure_ascii=False)

    assert judgment is True


def test_monju_step_by_step(run_api):

    judgment = True

    params = pack_parameters(theme=THEME,
                             ideas=IDEAS,
                             freedom=FREEDOM,
                             language=LANGUAGE)
    bs = Monju(api_keys=API_KEY, verbose=True, **params)

    try:
        if run_api:
            print(f"Status: {bs.status}")
            bs.generate_ideas()
            print(f"Status: {bs.status}")
            bs.organize_ideas()
            print(f"Status: {bs.status}")
            bs.evaluate_ideas()
            print(f"Status: {bs.status}")
            bs.verify()
            print(f"Status: {bs.status}")
    except Exception as e:
        pytest.fail(f'Error: {e}')

    print(f'Result:\n{json.dumps(bs.record, indent=2)}')

    with open('monju_sbs.json', 'w', encoding='utf-8') as f:
        json.dump(bs.record, f, indent=2, ensure_ascii=False)

    assert judgment is True
