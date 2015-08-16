from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from astroid import MANAGER, Class

from .models import transform_model_class


def register(linter):
    MANAGER.register_transform(Class, transform_model_class)
