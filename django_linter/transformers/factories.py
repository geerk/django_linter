from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers.utils import safe_infer
from astroid import MANAGER, Class, Name, Instance, YES
from astroid.builder import AstroidBuilder


try:
    DjangoModel = AstroidBuilder(MANAGER).string_build("""
from django.db import models
class Model(models.Model):
    id = models.AutoField()""").lookup('Model')[1][0]
except IndexError:
    DjangoModel = None


def transform_factory_return(node):
    if (isinstance(node.func, Name) and
            'factory' in node.func._repr_name().lower()):
        val = safe_infer(node.func)
        if (isinstance(val, Class) and
                val.is_subtype_of('factory.django.DjangoModelFactory')):
            try:
                model = safe_infer(val.locals['Meta'][0].locals['model'][0])
            except (KeyError, IndexError):
                pass
            else:
                if model is not None and model is not YES:
                    if isinstance(model, Class):
                        def infer_call_result(self, caller, context=None):
                            yield Instance(model)
                        val.infer_call_result = infer_call_result
                elif DjangoModel is not None:
                    def infer_call_result(self, caller, context=None):
                        yield Instance(DjangoModel)
                    val.infer_call_result = infer_call_result
