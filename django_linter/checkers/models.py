from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import safe_infer
from astroid import YES, AssName, Keyword, Return, Getattr, Instance, Name


class ModelsChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'models'
    msgs = {
        'W5101': ('Text field is nullable: %s',
                  'nullable-text-field',
                  'Used when text field has null=True.'),
        'W5102': ('Money related field is float: %s',
                  'float-money-field',
                  'Used when money related field uses FloatField.'),
        'W5103': ('Possible use of naive datetime, consider using "auto_now"',
                  'naive-datetime-used',
                  'Used when there is datetime.now is used.'),
        'W5104': ('Related field is named with _id suffix',
                  'related-field-named-with-id',
                  'Used when related field is named with _id suffix'),
        'W5105': ('Unicode method is absent in model "%s"',
                  'unicode-method-absent',
                  'Used when model has no unicode method.'),
        'W5106': ('Unicode method should always return unicode',
                  'unicode-method-return',
                  'Used when unicode method does not return unicode.'),
        'W5107': ('Model field redefinition: %s.%s',
                  'model-field-redefinition',
                  'Used when there are more than one model field with '
                  'the same name.'),
        'W5108': ('get_absolute_url defined without using reverse (%s)',
                  'get-absolute-url-without-reverse',
                  'Used when get_absolute_url method is defined without using '
                  'reverse function.'),
    }

    _is_model_class = False
    _has_unicode_method = False
    _is_get_absolute_url = False
    _is_reverse_used_in_get_absolute_url = False
    _text_fields = {'django.db.models.fields.CharField',
                    'django.db.models.fields.TextField',
                    'django.db.models.fields.SlugField'}

    @staticmethod
    def _is_money_field(field_name):
        return 'price' in field_name

    @classmethod
    def _is_text_field(cls, klass):
        return any(klass.is_subtype_of(text_field)
                   for text_field in cls._text_fields)

    @classmethod
    def _is_text_class(cls, klass):
        return (klass.is_subtype_of('__builtin__.unicode')
                or cls._is_text_field(klass))

    def visit_class(self, node):
        self._is_model_class = bool(
            node.is_subtype_of('django.db.models.base.Model'))
        if self._is_model_class:
            self._model_field_names = set()
            self._model_name = node.name

    def leave_class(self, node):
        if self._is_model_class and not self._has_unicode_method:
            self.add_message('W5105', args=node.name, node=node)

        self._is_model_class = False
        self._has_unicode_method = False

    def visit_function(self, node):
        if self._is_model_class:
            if node.name == '__unicode__':
                self._has_unicode_method = True
                for stmt in node.body:
                    if isinstance(stmt, Return):

                        val = safe_infer(stmt.value)
                        if (val and isinstance(val, Instance) and
                                not self._is_text_class(val._proxied)):
                            self.add_message('W5106', node=stmt)

                        elif isinstance(stmt.value, Getattr):
                            getattr_ = stmt.value
                            if getattr_.expr.name == 'self':
                                if getattr_.attrname == 'id':
                                    self.add_message('W5106', node=stmt)
            elif node.name == 'get_absolute_url':
                self._is_get_absolute_url = True

    def leave_function(self, node):
        if (self._is_get_absolute_url and
                not self._is_reverse_used_in_get_absolute_url):
            self.add_message('W5108', node=node, args=(self._model_name,))
        self._is_reverse_used_in_get_absolute_url = False
        self._is_get_absolute_url = False

    def visit_callfunc(self, node):
        if (self._is_get_absolute_url and isinstance(node.func, Name) and
                node.func.name == 'reverse'):
            self._is_reverse_used_in_get_absolute_url = True

        if self._is_model_class:
            ass_name = node.parent.get_children().next()
            if isinstance(ass_name, AssName):
                field_name = ass_name.name
                val = safe_infer(node)
                if val is not None and val is not YES:
                    if val.is_subtype_of('django.db.models.fields.Field'):
                        if field_name in self._model_field_names:
                            self.add_message(
                                'W5107', node=node,
                                args=(self._model_name, field_name))
                        else:
                            self._model_field_names.add(field_name)

                        if val.name in self._text_fields:
                            for arg in node.args:
                                if (isinstance(arg, Keyword) and
                                        arg.arg == 'null' and arg.value.value):
                                    self.add_message('W5101', args=field_name,
                                                     node=arg.value)
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
                            self.add_message(
                                'W5102', args=field_name, node=node)
