from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pylint.checkers.classes import ClassChecker
from pylint.checkers.base import DocStringChecker
from pylint.checkers.design_analysis import MisdesignChecker
from pylint.checkers.newstyle import NewStyleConflictChecker

from .suppress import suppress_msgs, is_meta_class


def register(linter):
    if 'good-names' in linter._all_options:
        linter.global_set_option('good-names', ','.join([
            # default
            'i', 'j', 'k', 'ex', 'Run', '_',
            # django specific
            'urlpatterns', 'qs', 'id',
            # misc
            'logger',
        ]))

    suppress_msgs(DocStringChecker, 'visit_classdef', is_meta_class,
                  'missing-docstring')
    suppress_msgs(MisdesignChecker, 'leave_classdef', is_meta_class,
                  'too-few-public-methods')
    suppress_msgs(NewStyleConflictChecker, 'visit_classdef', is_meta_class,
                  'old-style-class')
    suppress_msgs(ClassChecker, 'visit_classdef', is_meta_class, 'no-init')
