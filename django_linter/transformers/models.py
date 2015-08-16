from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from astroid import MANAGER, Class, Instance, Function, Arguments, Pass


def transform_model_class(cls):
    if cls.is_subtype_of('django.db.models.base.Model'):
        core_exceptions = MANAGER.ast_from_module_name('django.core.exceptions')
        # add DoesNotExist exception
        DoesNotExist = Class('DoesNotExist', None)
        DoesNotExist.bases = core_exceptions.lookup('ObjectDoesNotExist')[1]
        cls.locals['DoesNotExist'] = [DoesNotExist]
        # add MultipleObjectsReturned exception
        MultipleObjectsReturned = Class('MultipleObjectsReturned', None)
        MultipleObjectsReturned.bases = core_exceptions.lookup(
            'MultipleObjectsReturned')[1]
        cls.locals['MultipleObjectsReturned'] = [MultipleObjectsReturned]
        # add objects manager
        if 'objects' not in cls.locals:
            try:
                Manager = MANAGER.ast_from_module_name(
                    'django.db.models.manager').lookup('Manager')[1][0]
                QuerySet = MANAGER.ast_from_module_name(
                    'django.db.models.query').lookup('QuerySet')[1][0]
            except IndexError:
                pass
            else:
                if isinstance(Manager.body[0], Pass):
                    # for django >= 1.7
                    for func_name, func_list in QuerySet.locals.items():
                        if (not func_name.startswith('_') and
                                func_name not in Manager.locals):
                            func = func_list[0]
                            if (isinstance(func, Function) and
                                    'queryset_only' not in func.instance_attrs):
                                f = Function(func_name, None)
                                f.args = Arguments()
                                Manager.locals[func_name] = [f]
                cls.locals['objects'] = [Instance(Manager)]
        # add id field
        if 'id' not in cls.locals:
            try:
                AutoField = MANAGER.ast_from_module_name(
                    'django.db.models.fields').lookup('AutoField')[1][0]
            except IndexError:
                pass
            else:
                cls.locals['id'] = [Instance(AutoField)]

