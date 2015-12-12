from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import safe_infer
from astroid import YES, AssName, Keyword, Return, Getattr, Instance, Name

from ..__pkginfo__ import BASE_ID


class ModelsChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'models'
    msgs = {
        'W%s41' % BASE_ID: (
            'Text field is nullable: %s',
            'nullable-text-field',
            'Used when text field has null=True.'),
        'W%s42' % BASE_ID: (
            'Money related field is float: %s',
            'float-money-field',
            'Used when money related field uses FloatField.'),
        'W%s43' % BASE_ID: (
            'Possible use of naive datetime, consider using "auto_now"',
            'naive-datetime-used',
            'Used when there is datetime.now is used.'),
        'W%s44' % BASE_ID: (
            'Related field is named with _id suffix',
            'related-field-named-with-id',
            'Used when related field is named with _id suffix'),
        'W%s45' % BASE_ID: (
            'Unicode method is absent in model "%s"',
            'unicode-method-absent',
            'Used when model has no unicode method.'),
        'W%s46' % BASE_ID: (
            'Unicode method should always return unicode',
            'unicode-method-return',
            'Used when unicode method does not return unicode.'),
        'W%s47' % BASE_ID: (
            'Model field redefinition: %s.%s',
            'model-field-redefinition',
            'Used when there are more than one model field with '
            'the same name.'),
        'W%s48' % BASE_ID: (
            'get_absolute_url defined without using reverse (%s)',
            'get-absolute-url-without-reverse',
            'Used when get_absolute_url method is defined without using '
            'reverse function.'),
    }

    _is_model_class = False
    _has_unicode_method = False
    _is_get_absolute_url = False
    _is_reverse_used_in_get_absolute_url = False
    _text_fields = {'CharField', 'TextField', 'SlugField'}

    @staticmethod
    def _is_money_field(field_name):
        return 'price' in field_name

    @classmethod
    def _is_text_field(cls, klass):
        return any(klass.is_subtype_of('django.db.models.fields.' + text_field)
                   for text_field in cls._text_fields)

    @classmethod
    def _is_text_class(cls, klass):
        return (klass.is_subtype_of('__builtin__.unicode')
                or cls._is_text_field(klass))

    def visit_classdef(self, node):
        self._is_model_class = bool(
            node.is_subtype_of('django.db.models.base.Model'))
        if self._is_model_class:
            self._model_field_names = set()
            self._model_name = node.name

    def leave_classdef(self, node):
        if self._is_model_class and not self._has_unicode_method:
            self.add_message('unicode-method-absent', args=node.name, node=node)

        self._is_model_class = False
        self._has_unicode_method = False

    def visit_functiondef(self, node):
        if self._is_model_class:
            if node.name == '__unicode__':
                self._has_unicode_method = True
                for stmt in node.body:
                    if isinstance(stmt, Return):

                        val = safe_infer(stmt.value)
                        if (val and isinstance(val, Instance) and
                                not self._is_text_class(val._proxied)):
                            self.add_message('unicode-method-return', node=stmt)

                        elif isinstance(stmt.value, Getattr):
                            getattr_ = stmt.value
                            if getattr_.expr.name == 'self':
                                if getattr_.attrname == 'id':
                                    self.add_message(
                                        'unicode-method-return', node=stmt)
            elif node.name == 'get_absolute_url':
                self._is_get_absolute_url = True

    def leave_functiondef(self, node):
        if (self._is_get_absolute_url and
                not self._is_reverse_used_in_get_absolute_url):
            self.add_message('get-absolute-url-without-reverse',
                             node=node, args=(self._model_name,))
        self._is_reverse_used_in_get_absolute_url = False
        self._is_get_absolute_url = False

    def visit_call(self, node):
        if (self._is_get_absolute_url and isinstance(node.func, Name) and
                node.func.name == 'reverse'):
            self._is_reverse_used_in_get_absolute_url = True

        if self._is_model_class:
            ass_name = next(node.parent.get_children())
            if isinstance(ass_name, AssName):
                field_name = ass_name.name
                val = safe_infer(node)
                if val is not None and val is not YES:
                    if val.is_subtype_of('django.db.models.fields.Field'):
                        if field_name in self._model_field_names:
                            self.add_message(
                                'model-field-redefinition', node=ass_name,
                                args=(self._model_name, field_name))
                        else:
                            self._model_field_names.add(field_name)

                        if val.name in self._text_fields:
                            for arg in node.keywords or []:
                                if (arg.arg == 'null' and arg.value.value):
                                    self.add_message(
                                        'nullable-text-field', args=field_name,
                                        node=arg.value)
                        elif val.name == 'DateTimeField':
                            for arg in node.keywords or []:
                                if (arg.arg == 'default' and
                                        'datetime.now' in arg.value.as_string()):
                                    self.add_message(
                                        'naive-datetime-used', node=arg.value)
                        elif val.is_subtype_of(
                                'django.db.models.fields.related.RelatedField'):
                            if field_name.endswith('_id'):
                                self.add_message('related-field-named-with-id',
                                                 node=ass_name)
                        if self._is_money_field(field_name) and (
                                val.name == 'FloatField'):
                            self.add_message(
                                'float-money-field', args=field_name,
                                node=ass_name)
