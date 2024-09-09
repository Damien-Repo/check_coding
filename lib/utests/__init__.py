import io
import unittest
import json
import os
import inspect

from lib.utils import PluginManager
from lib.config import Config
from lib.check_coding import CheckCoding
from lib.source_file import SourceFilePos


#//TEMP voir pour faire un Mock pour les file
#//TEMP gerer des file physique (present dans un folder files/ a cote des tests)
#//TEMP gerer des faux file rempli a partir d'une string
#//TEMP le Mock doit fournir un fichier du meme type que celui qui sort de argparse ou api equivalent

class MockFile(io.TextIOWrapper):

    def __init__(self, file_name, file_content=None):
        cur_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(cur_frame, 2)
        for caller in caller_frame:
            if caller.filename.endswith('__init__.py'):
                continue
            root_path = os.path.dirname(os.path.realpath(caller.filename))
            file_path = os.path.join(root_path, 'files', file_name)
            break

        if file_content is None:
            # real file
            super().__init__(io.FileIO(file_path))
        else:
            # fake file
            super().__init__(io.BytesIO(file_content.encode()))

        self._name = file_path

    def __getattribute__(self, name):
        if name == 'name':
            return self._name
        return super().__getattribute__(name)


class UTest(unittest.TestCase):

    _orig_conf = {}

    def __init__(self, json_conf, verbose=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._cur_test_conf = None

        # Enforce outcome
        whitelist = ['default.OutcomeUTest']
        if verbose:
            whitelist.append('default.OutcomeTqdm')
        data_to_update = {
            'Outcome': {
                'WHITELIST': whitelist,
                'BLACKLIST': [],
            }
        }
        Config().update_from_data(data_to_update)

    @classmethod
    def setUpClass(cls) -> None:
        #print('===>>> setUpClass', cls)
        pass

    def setUp(self) -> None:
        self._check_cls_name = self.__class__.__name__.rsplit('Test', 1)[0]
        sec_name, module = self.__module__.rsplit('.', 1)[0].split(f'.utests.', 1)[1].split('.', 1)
        conf_sec_name = sec_name.capitalize()[:-1]
        self._check_name = self.id().rsplit('.', 1)[1].replace('test_', '', 1)
        normalized_name = f'{module}.{self._check_cls_name}.{self._check_name}'

        self._cur_test_conf = json.loads(Config().dump(mode='json'))
        conf_name = list(self._cur_test_conf.keys())[0]
        self._cur_test_conf[conf_name][conf_sec_name]['WHITELIST'] = [normalized_name]
        self._cur_test_conf[conf_name][conf_sec_name]['BLACKLIST'] = []

    def check(self, file_name, should_succeed=True):
        conf_file = MockFile('custom_conf.json', json.dumps(self._cur_test_conf))
        cc = CheckCoding(config_file=conf_file, files_to_check=[file_name])
        self.outcome = cc.get_outcome('OutcomeUTest')
        assert(self.outcome is not None)
        self.assertEqual(cc.has_succeeded, should_succeed)

    def check_from_file(self, file_name, file_content=None, should_succeed=True):
        with MockFile(file_name, file_content) as f:
            self.check(f, should_succeed)

    def check_exception(self, exception, assert_func):
        exception.checker_name = self._check_cls_name
        exception._check_name = self._check_name
        exception._context_pos = SourceFilePos(
                exception.error_pos.line_start,
                0,
                exception.error_pos.line_end,
                exception.error_pos.col_end,
        )

        assert_func(exception, self.outcome)

    def check_exception_in(self, exception):
        self.check_exception(exception, self.assertIn)

    def check_exception_not_in(self, exception):
        self.check_exception(exception, self.assertNotIn)

    def tearDown(self) -> None:
        self._cur_test_conf = None


class UTestManager(PluginManager):

    def __init__(self, config_file, dump_conf=None, verbose=False, **__):
        super().__init__()

        json_conf = Config(reset=True, conf_file=config_file).dump(mode='json')
        if dump_conf is not None:
            print(f'{Config().dump(dump_conf)}')
            print('-' * 70)

        suite = unittest.TestSuite()
        plugins = {
            'checker': Config().Checker,
            'loader': Config().Loader,
            'outcome': Config().Outcome,
        }

        for name, conf in plugins.items():
            extra = {
                'prefix': f'{name}_',
                'whitelist': conf.WHITELIST,
                'blacklist': conf.BLACKLIST,
                'create_plugin_instance': False,
            }
            self.load_plugins(UTest, os.path.join('lib', 'utests', f'{name}s'), **extra)
            self.load_plugins(UTest, os.path.join(Config().CUSTOM_ROOT_PATH, 'utests', f'{name}s'), **extra)

            for cls_name, Test in self:
                cls_name = cls_name.rsplit('Test', 1)[0]
                module = Test.__module__.split(f'.{name}s.', 1)[1].rsplit('.', 1)[0]
                for test_name in [k for k in Test.__dict__.keys() if k.startswith('test_')]:
                    normalized_name = f'{module}.{cls_name}.{test_name.replace("test_", "", 1)}'
                    if self._is_allowed(normalized_name, conf.WHITELIST, conf.BLACKLIST):
                        suite.addTest(Test(json_conf, verbose, test_name))

            self._plugins = {}

        runner = unittest.TextTestRunner()
        res = runner.run(suite)

        self.has_succeeded = False
        if len(res.errors) > 0 or len(res.failures) > 0:
            self.has_succeeded = True
