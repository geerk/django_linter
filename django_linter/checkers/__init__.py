from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from . import settings, models, misc, layout, forms, views


def register(linter):
    linter.register_checker(settings.SettingsShecker(linter))
    linter.register_checker(models.ModelsChecker(linter))
    linter.register_checker(misc.MiscChecker(linter))
    linter.register_checker(layout.LayoutChecker(linter))
    linter.register_checker(forms.FormsChecker(linter))
    linter.register_checker(views.ViewsChecker(linter))
