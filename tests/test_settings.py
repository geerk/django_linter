from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys
from unittest import TestCase
from os.path import abspath, dirname, join

from pylint.testutils import linter


class SettingsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        DATA = join(dirname(abspath(__file__)), 'settings')
        sys.path.insert(1, DATA)

    def setUp(self):
        linter.reporter.finalize()

    def test_required_setting_missed(self):
        linter.check('settings.required.settings')
        got = linter.reporter.finalize().strip()
        self.assertEqual(
            got, """E:  1: Required setting "ALLOWED_HOSTS" is missed
E:  1: Required setting "STATIC_ROOT" is missed""")

    def test_empty_settings(self):
        linter.check('settings.empty.settings')
        got = linter.reporter.finalize().strip()
        self.assertEqual(
            got, '''E:  5: Empty setting "ALLOWED_HOSTS"
E:  6: Empty setting "STATIC_ROOT"''')
