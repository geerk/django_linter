from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer
from pylint.interfaces import IAstroidChecker
from astroid import YES, List

from ..__pkginfo__ import BASE_ID


class SettingsShecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'settings'
    msgs = {
        'E%s21' % BASE_ID: (
            'Required setting "%s" is missed',
            'required-setting-missed',
            'Used when required setting missed in settings file.'),
        'E%s22' % BASE_ID: (
            'Empty setting "%s"',
            'empty-setting',
            'Used when setting is empty value.'),
        'W%s21' % BASE_ID: (
            'Improper settings import',
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
            self.add_message('improper-settings-import', node=node)

    def visit_from(self, node):
        if node.modname.rsplit('.', 1)[-1] == 'settings' or (
                'settings' in dict(node.names) and
                'django.conf' not in node.modname):
            self.add_message('improper-settings-import', node=node)

    def leave_module(self, node):
        if self._is_settings_module(node):
            module_locals = node.locals
            for setting_name in self._REQUIRED_SETTINGS:
                if setting_name not in module_locals:
                    self.add_message(
                        'required-setting-missed', args=setting_name, node=node)
                else:
                    setting = module_locals[setting_name][-1]
                    val = safe_infer(setting)
                    if val is not None and val is not YES:
                        if isinstance(val, List):
                            is_empty = not val.elts
                        else:
                            is_empty = not val.value
                        if is_empty:
                            self.add_message('empty-setting', args=setting_name,
                                             node=setting)
