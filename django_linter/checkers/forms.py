from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import safe_infer
from astroid import YES, AssName


class FormsChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'forms'
    msgs = {
        'W5401': ('Form field redefinition: %s.%s',
                  'form-field-redefinition',
                  'Used when there are more than one form field with '
                  'the same name.'),
    }

    _is_form_class = False

    def visit_class(self, node):
        self._is_form_class = bool(
            node.is_subtype_of('django.forms.forms.BaseForm'))
        if self._is_form_class:
            self._form_field_names = set()
            self._form_name = node.name

    def leave_class(self, node):
        self._is_form_class = False

    def visit_callfunc(self, node):
        if self._is_form_class:
            ass_name = next(node.parent.get_children())
            if isinstance(ass_name, AssName):
                field_name = ass_name.name
                val = safe_infer(node)
                if val is not None and val is not YES:
                    if val.is_subtype_of('django.forms.fields.Field'):
                        if field_name in self._form_field_names:
                            self.add_message(
                                'W5401', node=node,
                                args=(self._form_name, field_name))
                        else:
                            self._form_field_names.add(field_name)
