from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import safe_infer
from astroid import AssName


class ModelsChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'models'
    msgs = {
        'W5101': ('Text field is nullable: %s',
                  'nullable-text-field',
                  'Used when text field has null=True.'),
        'W5102': ('Money related field is float: %s',
                  'float-money-field',
                  'Used when money related field uses FloatField'),
    }

    _is_model_class = False
    _test_fields = {'CharField', 'TextField', 'SlugField'}

    @staticmethod
    def _is_money_field(field_name):
        return 'price' in field_name

    def visit_class(self, node):
        self._is_model_class = bool(
            node.is_subtype_of('django.db.models.base.Model'))

    def leave_class(self, node):
        self._is_model_class = False

    def visit_callfunc(self, node):
        if self._is_model_class:
            ass_name = node.parent.get_children().next()
            field_name = 'undefined'
            if isinstance(ass_name, AssName):
                field_name = ass_name.name
            val = safe_infer(node)
            if val is not None:
                if val.name in self._test_fields:
                    for arg in node.args:
                        if arg.arg == 'null' and arg.value.value:
                            self.add_message(
                                'W5101', args=field_name, node=node)
                if self._is_money_field(field_name) and (
                        val.name == 'FloatField'):
                    self.add_message('W5102', args=field_name, node=node)
