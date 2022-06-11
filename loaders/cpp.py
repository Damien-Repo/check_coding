#!/usr/bin/env python

import subprocess

from .loader import Loader, ILoaderLine


class LoaderLinePP(ILoaderLine):

    def __str__(self):
        return self.line.replace('\n', '')


class LoaderPP(Loader):

    LOADER_LINE = LoaderLinePP
    CPP_FLAGS = ''

    @property
    def pp_cmd(self):
        return f'cpp {self.__class__.CPP_FLAGS} {self.file_name}'

    @staticmethod
    def clean_line(line, line_inc=1, context={}):
        if 'line_num' in context:
            del(context['line_num'])
        if line.startswith('# '):
            tokens = line.strip().split(' ')
            line_num, filename = tokens[1:3]
            if line_num.isnumeric():
                context['line_num'] = int(line_num)
                flags = tokens[3:]
                context['skip'] = '3' in flags or \
                                  '2' in flags or \
                                  filename in ['"<built-in>"', '"<command-line>"']
            line = None
            line_inc = 0

        skip = context.get('skip', False)
        line = None if skip else line
        line_inc = 0 if skip else line_inc
        return line, line_inc, context

    def _parse(self):
        proc = subprocess.Popen(self.pp_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        line_num = 1
        ctx = {}
        for line in proc.stdout:
            line = line.decode('utf-8')
            line, line_inc, ctx = self.clean_line(line, context=ctx)
            line_num = ctx.get('line_num', line_num)
            if line is not None:
                self.append_line(line, line_num=line_num)
                line_num += line_inc


class LoaderPPKeepComment(LoaderPP):
    CPP_FLAGS = '-CC'


if __name__ == '__main__':
    pass
