import ast
import os
import sys
from _ast import Import, ImportFrom, alias
from ast import NodeTransformer as Transformer
from typing import Any

UNITTEST = 'unittest'
WRAPPER_BASE = 'TestWrapper.WrapperBase'


class InputTransformer(Transformer):

    def visit_Import(self, node: Import) -> Any:
        names = list(((n.name, n.asname) for n in node.names))
        for (n, asn) in names:
            if UNITTEST == n.split('.')[0]:
                old_aliases = list(filter(lambda e: UNITTEST != e.name.split('.')[0], node.names))
                if asn:
                    unittest_alias = alias(name=n.replace(UNITTEST, WRAPPER_BASE), asname=asn)
                else:
                    unittest_alias = alias(name=WRAPPER_BASE, asname=UNITTEST)
                return Import(old_aliases + [unittest_alias])
        return node

    def visit_ImportFrom(self, node: ImportFrom) -> Any:
        if node.module.split('.')[0] == UNITTEST:
            module_name = node.module.replace(UNITTEST, WRAPPER_BASE)
            return ImportFrom(module_name, node.names, node.level)
        return node


assert os.path.exists(sys.argv[1])

file_path = os.path.abspath(sys.argv[1])

with open(file_path, 'rt') as f:
    file_text = f.read()

parsed = ast.parse(file_text)
t = InputTransformer()
t.visit(parsed)

with open(file_path, 'wt') as f:
    f.write(ast.unparse(parsed))
