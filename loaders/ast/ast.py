#!/usr/bin/env python

import subprocess

from loaders.loader import Loader, ILoaderLine


class LoaderLineAST(ILoaderLine):

    def __str__(self):
        return self.line.replace('\n', '')


class ASTNode:
    PATTERN = None
    PATTERN_PAYLOAD = None

    def __init__(self, data_str):
        assert self.PATTERN, 'PATTERN should be defined'
        assert 'depth_str' and 'type' and 'addr' and 'payload' in self.PATTERN.pattern
        self._data = data_str.replace('\n', '')
        match = self.PATTERN.match(self._data)
        assert match, f'Not match {self.PATTERN} for "{self._data}"'
        self._depth_str = match.group('depth_str')
        self.type = match.group('type')
        self.addr = match.group('addr')
        self._dict = self.parse_payload(match.group('payload'))

        self.parent = None
        self.children = []

    def __getattr__(self, item):
        if item in self._dict:
            return self._dict[item]

    def parse_payload(self, payload):
        if self.PATTERN_PAYLOAD is None:
            return {}

        match = self.PATTERN_PAYLOAD.match(payload)
        assert match, f'Not match {self.PATTERN_PAYLOAD} for "{payload}"'
        return match.groupdict()

    @property
    def depth(self):
        return 0 if self._depth_str is None else len(self._depth_str) // 2

    def __str__(self):
        return f'{self.type} {self.addr}'

    def dump(self, indent=0):
        padding = '  ' * indent
        print(f'{padding}{self}')
        for child in self.children:
            child.dump(indent + 1)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self


class ASTNodeFactory:

    AST_NODE = ASTNode
    PATTERN_TYPE = None

    def __new__(cls, data_str):
        assert cls.PATTERN_TYPE, 'PATTERN_TYPE should be defined'
        match = cls.PATTERN_TYPE.match(data_str)
        assert match, f'Not match {cls.PATTERN_TYPE} for "{data_str}"'
        cls_type = match.group("type")
        node = cls.get_class_from_name(cls_type)
        if node is not None:
            return node(data_str)

        return cls.AST_NODE(data_str)

    @classmethod
    def get_class_from_name(cls, name):
        def _rec(node_cls):
            n_name = node_cls.__name__[len(cls.AST_NODE.__name__):]
            out = None
            if name.endswith(n_name):
                out = node_cls

            for child_node_cls in node_cls.__subclasses__():
                o = _rec(child_node_cls)
                if o is not None:
                    return o

            return out

        return _rec(cls.AST_NODE)

class LoaderAST(Loader):

    LOADER_LINE = LoaderLineAST
    AST_NODE_FACTORY = ASTNodeFactory
    AST_CMD = None

    @property
    def ast_cmd(self):
        assert self.AST_CMD, 'AST_CMD should be defined'
        return self.AST_CMD.format(**locals())

    def _parse(self):
        proc = subprocess.Popen(self.ast_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        root_node = prev_node = None
        for line in proc.stdout:
            line = line.decode('utf-8')
            node = self.AST_NODE_FACTORY(line)
            if root_node is None:
                root_node = node
            if prev_node is None:
                prev_node = node
            elif node.depth > prev_node.depth:
                prev_node.add_child(node)
                prev_node = node
            else:
                while prev_node.depth >= node.depth:
                    prev_node = prev_node.parent
                prev_node.add_child(node)
                prev_node = node

        print('===========================')
        root_node.dump()
        #//TEMP transformer les node en line pour le Loader


if __name__ == '__main__':
    pass
