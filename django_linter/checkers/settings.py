from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer
from pylint.interfaces import IAstroidChecker
from astroid import List


class SettingsShecker(BaseChecker):
    __implements__ = IAstroidChecker
    name = 'settings'
    msgs = {
        'E5001': ('Required setting "%s" is missed',
                  'required-setting-missed',
                  'Used when required setting missed in settings file.'),
        'E5002': ('Empty setting "%s"',
                  'empty-setting',
                  'Used when setting is empty value.'),
        'W5001': ('Improper settings import',
                  'improper-settings-import',
                  'Used when settings is not imported from django.conf'),
    }

    _REQUIRED_SETTINGS = ('STATIC_ROOT', 'ALLOWED_HOSTS')

    @staticmethod
    def _is_settings_module(node):
        if node.name.rsplit('.', 1)[-1] == 'settings':
            return True
        return False

    def visit_import(self, node):
        if ('settings' in node.as_string() and
                'django.conf' not in node.as_string()):
            self.add_message('W5001', node=node)

    def visit_from(self, node):
        if node.modname.rsplit('.', 1)[-1] == 'settings' or (
                'settings' in dict(node.names) and
                'django.conf' not in node.modname):
            self.add_message('W5001', node=node)

    def leave_module(self, node):
        if self._is_settings_module(node):
            module_locals = node.locals
            for setting_name in self._REQUIRED_SETTINGS:
                if setting_name not in module_locals:
                    self.add_message('E5001', args=setting_name, node=node)
                else:
                    value = safe_infer(module_locals[setting_name][-1])
                    if value:
                        if isinstance(value, List):
                            is_empty = not value.elts
                        else:
                            is_empty = not value.value
                        if is_empty:
                            self.add_message(
                                'E5002', args=setting_name, node=node)
