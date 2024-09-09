import sys
import inspect

from lib.log import Log
from lib.config import Config
from lib.source_file import SourceFile
from lib.checkers import CheckerManager


class CheckCoding:

    def __init__(self, config_file, **kwargs):
        self.has_succeeded = None

        try:
            Config(conf_file=config_file)

            steps = sorted([(name, func) for name, func in inspect.getmembers(self) if name.startswith('step_')])
            with Log().progress('Steps', len(steps), ' step') as log:
                for step_name, step_func in steps:
                    log.progress_set_name(f'{step_name.split("_", 2)[2]}')
                    if step_func(**kwargs) is False:
                        self.has_succeeded = False
                        Log().debug(f'Step {step_name} returned False')
                        break
                    log.progress_update()

        except KeyboardInterrupt:
            pass

    @staticmethod
    def step_010_dump_conf(dump_conf=None, **__):
        if dump_conf is not None:
            Log().print('=== Config begin ===')
            Log().print(f'{Config().dump(dump_conf)}')
            Log().print('=== Config end ===')

    def step_020_load_files(self, files_to_check=[], **__):
        # remove duplicates file name
        #files_to_check = {f.name: f for f in files_to_check}.values()

        self._src_files = []
        with Log().progress('Loading files', len(files_to_check), ' file') as log:
            for f in files_to_check:
                log.progress_set_name(f.name)
                self._src_files.append(SourceFile(f))
                log.progress_update()

        if len(self._src_files) == 0:
            Log().error('No files to check')
            return False

    def step_050_check_files(self, **__):
        checkers = CheckerManager()
        with Log().progress('Checking files', len(self._src_files), ' file') as log:
            for src_file in self._src_files:
                log.progress_set_name(src_file)
                checkers.process(src_file)
                result = checkers.get_result()
                if len(result) > 0:
                    self.has_succeeded = False
                log.set_result(result)
                log.progress_update()

        if self.has_succeeded is None:
            self.has_succeeded = True

    @staticmethod
    def get_outcome(name):
        try:
            return Log().get_outcome(name)
        except KeyError:
            print(f"Error: unknown outcome '{name}'", file=sys.stderr)
