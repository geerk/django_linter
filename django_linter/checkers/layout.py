from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from ..__pkginfo__ import BASE_ID


class LayoutChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'layout'
    msgs = {
        'W%s01' % BASE_ID: (
            'Form %s not in forms module',
            'forms-layout',
            'Used when form class definition is not in forms module.'),
        'W%s02' % BASE_ID: (
            'Admin class %s not in admin module',
            'admin-layout',
            'Used when admin class definition is not in admin module.'),
    }

    def leave_class(self, node):
        if node.is_subtype_of('django.forms.forms.BaseForm'):
            if not ('forms' in node.root().file):
                self.add_message('forms-layout', node=node, args=(node.name,))
        elif node.is_subtype_of('django.contrib.admin.options.ModelAdmin'):
            if not ('admin' in node.root().file):
                self.add_message('admin-layout', node=node, args=(node.name,))
