from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from . import checkers


def register(linter):
    checkers.register(linter)
