from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import safe_infer
from astroid import AssName, Keyword


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
        'W5103': ('Possible use of naive datetime, consider using "auto_now"',
                  'naive-datetime-used',
                  'Used when there is datetime.now is used.'),
        'W5104': ('Related field is named with _id suffix',
                  'related-field-named-with-id',
                  'Used when related field is named with _id suffix'),
    }

    _is_model_class = False
    _text_fields = {'CharField', 'TextField', 'SlugField'}

    @staticmethod
    def _is_money_field(field_name):
        return 'price' in field_name

    def visit_class(self, node):
        self._is_model_class = bool(
            node.is_subtype_of('django.db.models.base.Model'))

        if self._is_model_class:
            pass

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
                if val.name in self._text_fields:
                    for arg in node.args:
                        if (isinstance(arg, Keyword) and
                                arg.arg == 'null' and arg.value.value):
                            self.add_message(
                                'W5101', args=field_name, node=arg.value)
                elif val.name == 'DateTimeField':
                    for arg in node.args:
                        if (isinstance(arg, Keyword) and
                                arg.arg == 'default' and
                                'datetime.now' in arg.value.as_string()):
                            self.add_message('W5103', node=arg.value)
                elif val.is_subtype_of(
                        'django.db.models.fields.related.RelatedField'):
                    if field_name.endswith('_id'):
                        self.add_message('W5104', node=node)
                if self._is_money_field(field_name) and (
                        val.name == 'FloatField'):
                    self.add_message('W5102', args=field_name, node=node)
