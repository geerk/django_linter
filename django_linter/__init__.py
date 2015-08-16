from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from . import checkers, suppressers, transformers


def register(linter):
    checkers.register(linter)
    suppressers.register(linter)
    transformers.register(linter)
