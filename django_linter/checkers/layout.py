from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class LayoutChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'layout'
    msgs = {
        'W5301': ('Form %s not in forms module',
                  'forms-layout',
                  'Used when form class definition is not in forms module.'),
        'W5302': ('Admin class %s not in admin module',
                  'admin-layout',
                  'Used when admin class definition is not in adin module.'),
    }

    def leave_class(self, node):
        if node.is_subtype_of('django.forms.forms.BaseForm'):
            if not ('forms' in node.root().file):
                self.add_message('W5301', node=node, args=(node.name,))
        elif node.is_subtype_of('django.contrib.admin.options.ModelAdmin'):
            if not ('admin' in node.root().file):
                self.add_message('W5302', node=node, args=(node.name,))
