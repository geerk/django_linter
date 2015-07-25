from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from astroid import Name, CallFunc


class ViewsChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'views'
    msgs = {
        'W5501': ('is_authenticated is not called',
                  'is-authenticated-not-called',
                  'Used when is_authenticated method is not called'),
    }

    def visit_getattr(self, node):
        if (isinstance(node.expr, Name) and node.expr.name == 'request' and
                node.attrname == 'is_authenticated' and
                not isinstance(node.parent, CallFunc)):
            self.add_message('W5501', node=node)
