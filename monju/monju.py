import json
import re

from llmmaster import LLMMaster

from .config import CLASS_DIAGRAM_GENERATION_PROMPT
from .config import DEFAULT_FREEDOM
from .config import DEFAULT_IDEAS
from .config import DEFAULT_LANGUAGE
from .config import DEFAULT_TEMPERATURE_CLASS_DIAGRAM
from .config import DEFAULT_TEMPERATURE_EVALUATION
from .config import DEFAULT_TEMPERATURE_MINDMAP
from .config import EVALUATION_PROMPT
from .config import IDEA_GENERATION_PROMPT
from .config import KEY_CLASS_DIAGRAM
from .config import KEY_ELAPSED_TIME
from .config import KEY_EVALUATION
from .config import KEY_FREEDOM
from .config import KEY_IDEAS
from .config import KEY_INPUT
from .config import KEY_LANGUAGE
from .config import KEY_MINDMAP
from .config import KEY_OUTPUT
from .config import KEY_THEME
from .config import LLM_CLASS_DIAGRAM
from .config import LLM_IDEA_EVALUATION
from .config import LLM_IDEA_GENERATION
from .config import LLM_MINDMAP
from .config import MINDMAP_GENERATION_PROMPT
from .config import PROGRESS_DONE
from .config import PROGRESS_FAILED
from .config import PROGRESS_IDEA_EVALUATION
from .config import PROGRESS_IDEA_GENERATION
from .config import PROGRESS_NOT_STARTED
from .config import PROGRESS_ORGANIZING
from .config import PROGRESS_VERIFYING


class Monju:
    '''
    Main class for Monju, multi-AI brainstorming framework.
    '''
    def __init__(self,
                 api_keys: str = '',
                 verbose: bool = False,
                 **kwargs):
        '''
        Initialize the Monju class with the following parameters:
          System parameters:
            api_keys (str): API keys for LLMs in LLMMaster manner
            verbose (bool): print progress for debugging
          Brainstorming parameters as kwargs:
            theme (str) (required): theme or topic of brainstorming
            ideas (int): number of ideas to generate
            freedom (float): freedom value for LLM
            language (str): language for output
        '''
        if not kwargs:
            raise ValueError('No parameters are given.')
        elif (not kwargs.get(KEY_THEME, None) or
              not isinstance(kwargs.get(KEY_THEME), str)):
            raise ValueError(f'{KEY_THEME} is not given or not str.')

        if (kwargs.get(KEY_IDEAS, None) is None or
           not isinstance(kwargs.get(KEY_IDEAS), int)):
            kwargs[KEY_IDEAS] = DEFAULT_IDEAS
        if (kwargs.get(KEY_FREEDOM, None) is None or
           not isinstance(kwargs.get(KEY_FREEDOM), float)):
            kwargs[KEY_FREEDOM] = DEFAULT_FREEDOM
        if (kwargs.get(KEY_LANGUAGE, None) is None or
           not isinstance(kwargs.get(KEY_LANGUAGE), str)):
            kwargs[KEY_LANGUAGE] = DEFAULT_LANGUAGE

        self.api_keys = api_keys
        self.verbose = verbose
        self.status = PROGRESS_NOT_STARTED
        self.record = {
            KEY_INPUT: kwargs,
            KEY_OUTPUT: {
                KEY_ELAPSED_TIME: []
            }
        }

    def brainstorm(self):
        '''
        Batch process of brainstorming
        '''
        try:
            self.generate_ideas()
            self.organize_ideas()
            self.evaluate_ideas()
            self.verify()
        except Exception as e:
            self.status = PROGRESS_FAILED
            raise Exception(e) from e

    def generate_ideas(self, **kwargs):
        '''
        Brainstorming Step 1: generate ideas
          kwargs: custom LLM setting in LLMMaster manner
        '''
        self.status = PROGRESS_IDEA_GENERATION

        if self.verbose:
            print('Monju Step 1: Generating ideas...')

        try:
            master = LLMMaster()
            master.set_api_keys(self.api_keys)
            master.summon(self._llm_ideation(**kwargs))
            master.run()

            for key, value in master.results.items():
                master.results[key] = self._remove_highlight(value)
            self.record[KEY_OUTPUT][KEY_IDEAS] = master.results
            self.record[KEY_OUTPUT][KEY_ELAPSED_TIME].append(
                master.elapsed_time)

        except Exception as e:
            self.status = PROGRESS_FAILED
            raise Exception(e) from e

    def organize_ideas(self, **kwargs):
        '''
        Brainstorming Step 2: organize ideas into mindmap and class diagram
          kwargs: custom LLM setting in LLMMaster manner
        '''
        self.status = PROGRESS_ORGANIZING

        if self.verbose:
            print('Monju Step 2: Organizing ideas...')

        try:
            master = LLMMaster()
            master.set_api_keys(self.api_keys)
            master.summon(self._llm_mindmap(**kwargs))
            master.summon(self._llm_class_diagram(**kwargs))
            master.run()

            self.record[KEY_OUTPUT][KEY_MINDMAP] = \
                self._sanitize_mermaid(master.results[KEY_MINDMAP])
            self.record[KEY_OUTPUT][KEY_CLASS_DIAGRAM] = \
                self._sanitize_mermaid(master.results[KEY_CLASS_DIAGRAM])
            self.record[KEY_OUTPUT][KEY_ELAPSED_TIME].append(
                master.elapsed_time)

        except Exception as e:
            self.status = PROGRESS_FAILED
            raise Exception(e) from e

    def evaluate_ideas(self, **kwargs):
        '''
        Brainstorming Step 3: evaluate ideas
          kwargs: custom LLM setting in LLMMaster manner
        '''
        self.status = PROGRESS_IDEA_EVALUATION

        if self.verbose:
            print('Monju Step 3: Evaluating ideas...')

        try:
            master = LLMMaster()
            master.set_api_keys(self.api_keys)
            master.summon(self._llm_evaluation(**kwargs))
            master.run()

            for key, value in master.results.items():
                master.results[key] = self._remove_highlight(value)
            self.record[KEY_OUTPUT][KEY_EVALUATION] = master.results
            self.record[KEY_OUTPUT][KEY_ELAPSED_TIME].append(
                master.elapsed_time)

        except Exception as e:
            self.status = PROGRESS_FAILED
            raise Exception(e) from e

    def verify(self):
        '''
        Brainstorming step 4: Verify if all the steps are completed
        Note: not necessary to check elapsed time
        '''
        self.status = PROGRESS_VERIFYING
        msg = ''

        if self.verbose:
            print('Monju Step 4: Verifying results...')
            print(f'Record:\n'
                  f'{json.dumps(self.record, indent=2, ensure_ascii=False)}')

        if not self.record[KEY_OUTPUT][KEY_IDEAS]:
            msg += 'Ideas are not generated. '
        if not self.record[KEY_OUTPUT][KEY_MINDMAP]:
            msg += 'Mindmap is not generated. '
        if not self.record[KEY_OUTPUT][KEY_CLASS_DIAGRAM]:
            msg += 'Class diagram is not generated. '
        if not self.record[KEY_OUTPUT][KEY_EVALUATION]:
            msg += 'Evaluation is not done. '

        if msg:
            self.status = PROGRESS_FAILED
            raise Exception("Error in verification: "+msg)

        self.status = PROGRESS_DONE

    def _llm_ideation(self, **kwargs):
        '''
        LLM configuration for idea generation.
        '''
        entries = kwargs.copy() if kwargs else LLM_IDEA_GENERATION.copy()

        self.record[KEY_INPUT][PROGRESS_IDEA_GENERATION] = entries

        prompt = IDEA_GENERATION_PROMPT.format(
            theme=self.record[KEY_INPUT][KEY_THEME],
            ideas=str(self.record[KEY_INPUT][KEY_IDEAS]),
            language=self.record[KEY_INPUT][KEY_LANGUAGE])

        if self.verbose:
            print(f'Prompt:\n{prompt}')

        for _, parameters in entries.items():
            parameters['prompt'] = prompt
            parameters['temperature'] = self.record[KEY_INPUT][KEY_FREEDOM]

        return entries

    def _llm_mindmap(self, **kwargs):
        '''
        LLM configuration for mindmap generation.
        '''
        entries = kwargs.copy() if kwargs else LLM_MINDMAP.copy()
        key = list(entries.keys())[0]
        entries = {KEY_MINDMAP: entries[key]}

        self.record[KEY_INPUT][KEY_MINDMAP] = entries

        idea_list = '\n'.join(self.record[KEY_OUTPUT][KEY_IDEAS].values())

        prompt = MINDMAP_GENERATION_PROMPT.format(
            theme=self.record[KEY_INPUT][KEY_THEME],
            idea_list=idea_list,
            language=self.record[KEY_INPUT][KEY_LANGUAGE])

        if self.verbose:
            print(f'Prompt:\n{prompt}')

        for _, parameters in entries.items():
            parameters['prompt'] = prompt
            parameters['temperature'] = DEFAULT_TEMPERATURE_MINDMAP

        return entries

    def _llm_class_diagram(self, **kwargs):
        '''
        LLM configuration for class diagram generation.
        '''
        entries = kwargs.copy() if kwargs else LLM_CLASS_DIAGRAM.copy()
        key = list(entries.keys())[0]
        entries = {KEY_CLASS_DIAGRAM: entries[key]}

        self.record[KEY_INPUT][KEY_CLASS_DIAGRAM] = entries

        idea_list = '\n'.join(self.record[KEY_OUTPUT][KEY_IDEAS].values())

        prompt = CLASS_DIAGRAM_GENERATION_PROMPT.format(
            theme=self.record[KEY_INPUT][KEY_THEME],
            idea_list=idea_list,
            language=self.record[KEY_INPUT][KEY_LANGUAGE])

        if self.verbose:
            print(f'Prompt:\n{prompt}')

        for _, parameters in entries.items():
            parameters['prompt'] = prompt
            parameters['temperature'] = DEFAULT_TEMPERATURE_CLASS_DIAGRAM

        return entries

    def _llm_evaluation(self, **kwargs):
        '''
        LLM configuration for idea evaluation.
        '''
        entries = kwargs.copy() if kwargs else LLM_IDEA_EVALUATION.copy()
        self.record[KEY_INPUT][PROGRESS_IDEA_EVALUATION] = entries

        prompt = EVALUATION_PROMPT.format(
            theme=self.record[KEY_INPUT][KEY_THEME],
            mermaid_mindmap=self.record[KEY_OUTPUT][KEY_MINDMAP],
            language=self.record[KEY_INPUT][KEY_LANGUAGE])

        if self.verbose:
            print(f'Prompt:\n{prompt}')

        for _, parameters in entries.items():
            parameters['prompt'] = prompt
            parameters['temperature'] = DEFAULT_TEMPERATURE_EVALUATION

        return entries

    def _sanitize_mermaid(self, source: str):
        '''
        Sanitize mermaid text to avoid errors.
        Strip markdown syntax and replace some characters for Japanese.
        '''
        pattern = r'^\s*```(\w+)\n(.*?)\n\s*```'
        match = re.match(pattern, source, re.DOTALL | re.MULTILINE)
        text = match[2]
        # text = text.replace('&', 'and')
        text = text.replace('・', '-')
        text = text.replace('(', '-')
        text = text.replace(')', '-')
        return text

    def _remove_highlight(self, source: str):
        '''
        Remove highlight syntax in evaluation text.
        '''
        return source.replace('**', '').replace('#', '')
