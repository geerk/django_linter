from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from astroid import MANAGER, Class

from .models import transform_model_class
from .testing import transform_test_response


def register(linter):
    MANAGER.register_transform(Class, transform_model_class)
    MANAGER.register_transform(Class, transform_test_response)
