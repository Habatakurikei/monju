import json
import re

from llmmaster import LLMMaster

from config import CLASS_DIAGRAM_GENERATION_PROMPT
from config import DEFAULT_FREEDOM
from config import DEFAULT_IDEAS
from config import DEFAULT_LANGUAGE
from config import DEFAULT_TEMPERATURE_CLASS_DIAGRAM
from config import DEFAULT_TEMPERATURE_EVALUATION
from config import DEFAULT_TEMPERATURE_MINDMAP
from config import EVALUATION_PROMPT
from config import IDEA_GENERATION_PROMPT
from config import KEY_CLASS_DIAGRAM
from config import KEY_ELAPSED_TIME
from config import KEY_EVALUATION
from config import KEY_FREEDOM
from config import KEY_IDEAS
from config import KEY_INPUT
from config import KEY_LANGUAGE
from config import KEY_MINDMAP
from config import KEY_OUTPUT
from config import KEY_THEME
from config import LLM_CLASS_DIAGRAM
from config import LLM_IDEA_EVALUATION
from config import LLM_IDEA_GENERATION
from config import LLM_MINDMAP
from config import MINDMAP_GENERATION_PROMPT
from config import PROGRESS_DONE
from config import PROGRESS_FAILED
from config import PROGRESS_IDEA_EVALUATION
from config import PROGRESS_IDEA_GENERATION
from config import PROGRESS_NOT_STARTED
from config import PROGRESS_ORGANIZING
from config import PROGRESS_VERIFYING


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
          Brainstorming parameters:
            theme (str): theme or topic of brainstorming
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
        elif (kwargs.get(KEY_FREEDOM, None) is None or
              not isinstance(kwargs.get(KEY_FREEDOM), float)):
            kwargs[KEY_FREEDOM] = DEFAULT_FREEDOM
        elif (kwargs.get(KEY_LANGUAGE, None) is None or
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

    def generate_ideas(self):
        '''
        Brainstorming step 1: Generate ideas
        '''
        self.status = PROGRESS_IDEA_GENERATION

        if self.verbose:
            print('Monju Step 1: Generating ideas...')

        try:
            master = LLMMaster()
            master.set_api_keys(self.api_keys)

            prompt = IDEA_GENERATION_PROMPT.format(
                theme=self.record[KEY_INPUT][KEY_THEME],
                ideas=str(self.record[KEY_INPUT][KEY_IDEAS]),
                language=self.record[KEY_INPUT][KEY_LANGUAGE])

            entries = LLM_IDEA_GENERATION.copy()
            for _, parameters in entries.items():
                parameters['prompt'] = prompt
                parameters['temperature'] = self.record[KEY_INPUT][KEY_FREEDOM]

            if self.verbose:
                print(f'Prompt:\n{prompt}')

            master.summon(entries)
            master.run()

            self.record[KEY_OUTPUT][KEY_IDEAS] = master.results
            self.record[KEY_OUTPUT][KEY_ELAPSED_TIME].append(
                master.elapsed_time)

            self.record[KEY_INPUT][PROGRESS_IDEA_GENERATION] = \
                LLM_IDEA_GENERATION

        except Exception as e:
            self.status = PROGRESS_FAILED
            raise Exception(e) from e

    def organize_ideas(self):
        '''
        Brainstorming step 2: Organize ideas into mindmap and class diagram
        '''
        self.status = PROGRESS_ORGANIZING

        if self.verbose:
            print('Monju Step 2: Organizing ideas...')

        try:
            master = LLMMaster()
            master.set_api_keys(self.api_keys)
            master.summon(self._mindmap_config())
            master.summon(self._class_diagram_config())
            master.run()

            self.record[KEY_OUTPUT][KEY_MINDMAP] = \
                self._sanitize_mermaid(master.results[KEY_MINDMAP])
            self.record[KEY_OUTPUT][KEY_CLASS_DIAGRAM] = \
                self._sanitize_mermaid(master.results[KEY_CLASS_DIAGRAM])
            self.record[KEY_OUTPUT][KEY_ELAPSED_TIME].append(
                master.elapsed_time)

            self.record[KEY_INPUT][KEY_MINDMAP] = LLM_MINDMAP
            self.record[KEY_INPUT][KEY_CLASS_DIAGRAM] = LLM_CLASS_DIAGRAM

        except Exception as e:
            self.status = PROGRESS_FAILED
            raise Exception(e) from e

    def evaluate_ideas(self):
        '''
        Brainstorming step 3: Evaluate ideas
        '''
        self.status = PROGRESS_IDEA_EVALUATION

        if self.verbose:
            print('Monju Step 3: Evaluating ideas...')

        try:
            master = LLMMaster()
            master.set_api_keys(self.api_keys)

            prompt = EVALUATION_PROMPT.format(
                theme=self.record[KEY_INPUT][KEY_THEME],
                mermaid_class=self.record[KEY_OUTPUT][KEY_CLASS_DIAGRAM],
                language=self.record[KEY_INPUT][KEY_LANGUAGE])

            entries = LLM_IDEA_EVALUATION.copy()
            for _, parameters in entries.items():
                parameters['prompt'] = prompt
                parameters['temperature'] = DEFAULT_TEMPERATURE_EVALUATION

            if self.verbose:
                print(f'Prompt:\n{prompt}')

            master.summon(entries)
            master.run()

            self.record[KEY_OUTPUT][KEY_EVALUATION] = master.results
            self.record[KEY_OUTPUT][KEY_ELAPSED_TIME].append(
                master.elapsed_time)

            self.record[KEY_INPUT][PROGRESS_IDEA_EVALUATION] = \
                LLM_IDEA_EVALUATION

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
            print('Monju Step 4: Verifying...')
            print(f'Record:\n{json.dumps(self.record, indent=2)}')

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
            raise Exception(msg)

        self.status = PROGRESS_DONE

    def _mindmap_config(self):

        idea_list = '\n'.join(self.record[KEY_OUTPUT][KEY_IDEAS].values())

        config = {
            KEY_MINDMAP: {
                'provider': LLM_MINDMAP['provider'],
                'model': LLM_MINDMAP['model'],
                'prompt': MINDMAP_GENERATION_PROMPT.format(
                    theme=self.record[KEY_INPUT][KEY_THEME],
                    idea_list=idea_list,
                    language=self.record[KEY_INPUT][KEY_LANGUAGE]),
                'temperature': DEFAULT_TEMPERATURE_MINDMAP
            }
        }

        if self.verbose:
            print(f'Prompt:\n{config[KEY_MINDMAP]["prompt"]}')

        return config

    def _class_diagram_config(self):

        idea_list = '\n'.join(self.record[KEY_OUTPUT][KEY_IDEAS].values())

        config = {
            KEY_CLASS_DIAGRAM: {
                'provider': LLM_CLASS_DIAGRAM['provider'],
                'model': LLM_CLASS_DIAGRAM['model'],
                'prompt': CLASS_DIAGRAM_GENERATION_PROMPT.format(
                    theme=self.record[KEY_INPUT][KEY_THEME],
                    idea_list=idea_list,
                    language=self.record[KEY_INPUT][KEY_LANGUAGE]),
                'temperature': DEFAULT_TEMPERATURE_CLASS_DIAGRAM
            }
        }

        if self.verbose:
            print(f'Prompt:\n{config[KEY_CLASS_DIAGRAM]["prompt"]}')

        return config

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
