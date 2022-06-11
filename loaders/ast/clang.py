#!/usr/bin/env python

import re

from .ast import LoaderAST, ASTNode, ASTNodeFactory


class ASTNodeClang(ASTNode):
    PATTERN = re.compile(r'^(?P<depth_str>[\s|`]+-)?(?P<type>[a-z]+) (?P<addr>0x[\da-f]+) (?P<payload>.*)$',
                         re.IGNORECASE)
    PATTERN_PAYLOAD = re.compile(r"(?P<all_default>.*)")

    def __str__(self):
        if getattr(self, 'all_default', False):
            return f'{self.__class__.__name__}: {super().__str__()} {self.all_default}'
        return super().__str__()

class ASTNodeClangStmt(ASTNodeClang):
    pass

class ASTNodeClangValueStmt(ASTNodeClangStmt):
    pass

class ASTNodeClangExpr(ASTNodeClangValueStmt):
    pass

class ASTNodeClangLiteral(ASTNodeClangExpr):
    pass

class ASTNodeClangType(ASTNodeClang):
    pass

class ASTNodeClangDecl(ASTNodeClang):
    pass

class ASTNodeClangNamedDecl(ASTNodeClangDecl):
    pass

class ASTNodeClangValueDecl(ASTNodeClangNamedDecl):
    pass

class ASTNodeClangDeclaratorDecl(ASTNodeClangValueDecl):
    pass

class ASTNodeClangFunctionDecl(ASTNodeClangDeclaratorDecl):
    PATTERN_PAYLOAD = re.compile(r"^(?:prev (?P<prev_addr>0x[\da-f]+) )?"
                                 r"<(?P<pos_start>[^,]+:\d+(:\d+)?)(?:, (?P<pos_end>[^>]+:\d+(:\d+)?))?>"
                                 r" (?P<name_pos>[^ ]+:\d+(:\d+)?)"
                                 r" (?:(?P<attributes>.+) )?(?P<name>[^ ]+) '(?P<prototype>[^']+)'(?: (?P<extra>.*))?$",
                                 re.IGNORECASE)

    def __str__(self):
        prev = '' if self.prev_addr is None else f'prev {self.prev_addr} '
        pos_end = '' if self.pos_end is None else f', {self.pos_end}'
        att = '' if self.attributes is None else f'{self.attributes} '
        extra = '' if self.extra is None else f' {self.extra}'
        return f'{super().__str__()} {prev}<{self.pos_start}{pos_end}>'\
               f" {self.name_pos} {att}{self.name} '{self.prototype}'{extra}"


class ASTNodeClangFactory(ASTNodeFactory):
    AST_NODE = ASTNodeClang
    PATTERN_TYPE = re.compile(r'^([\s|`]+-)?(?P<type>[a-z]+) 0x', re.IGNORECASE)


class LoaderASTClang(LoaderAST):
    AST_NODE_FACTORY = ASTNodeClangFactory
    AST_CMD = 'clang -Xclang -ast-dump -fno-diagnostics-color -fsyntax-only {self.file_name}'


if __name__ == '__main__':
    pass
