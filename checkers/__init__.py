import sys
import os
import importlib
import importlib.util

from log import OutputLog
from time import sleep   #//TEMP


class Checkers:

    def __init__(self):
        self._checkers = []
        self._result = []

        spec = importlib.util.find_spec('checkers.custom.base')   #//TEMP parcourir folder pour find all
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        classes = [c for c in module.__dict__.keys() if c.startswith('Checker')]
        for c in classes:
            self._checkers.append(getattr(module, c))
        '''
        p = sys.modules['checkers'].__path__[0]
        print(os.listdir(p))
        for f in os.listdir(p):
            if f.startswith('__'):
                continue
            fp = os.path.join(p, f)
            if not os.path.isdir(fp):
                continue
            print(fp)
        checkers = [k.replace('checkers.', '') for k in sys.modules.keys() if k.startswith('checkers.')]
        print(checkers)
        '''
        #print(self._checkers)

    def process(self, src_file):
        self._result = []
        with OutputLog().progress('Check', len(self._checkers), ' checker') as log:
            for Checker in self._checkers:
                log.progress_set_name(Checker.__name__)
                c = Checker(src_file)
                c.process()
                self._result.append(c)
                log.progress_update()

    def get_result(self):
        out_res = {}
        for checker in self._result:
            checker_name = checker.__class__.__name__
            for check_name, src_line, msg in checker.get_result():
                if src_line.row not in out_res:
                    out_res[src_line.row] = {}
                if checker_name not in out_res[src_line.row]:
                    out_res[src_line.row][checker_name] = {}
                assert(check_name not in out_res[src_line.row][checker_name])
                out_res[src_line.row][checker_name][check_name] = {
                    'message': msg,
                    'line': src_line,
                }

        return out_res
