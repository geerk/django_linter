from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__all__ = ('register',)


def register(linter):
    from .settings import SettingsShecker
    from .models import ModelsChecker

    linter.register_checker(SettingsShecker(linter))
    linter.register_checker(ModelsChecker(linter))
