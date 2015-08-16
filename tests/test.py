from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import unittest
import os

from pylint.testutils import make_tests, LintTestUsingFile, cb_test_gen, linter


def suite():
    input_dir = os.path.join(os.path.dirname(__file__), 'input')
    msg_dir = os.path.join(os.path.dirname(__file__), 'messages')
    linter.load_plugin_modules(['django_linter'])
    linter.global_set_option('required-attributes', ())
    linter.set_option('disable', 'R0901,C0111')
    return unittest.TestSuite([
        unittest.makeSuite(test, suiteClass=unittest.TestSuite)
        for test in make_tests(
            input_dir, msg_dir, None, [cb_test_gen(LintTestUsingFile)])])


def load_tests(loader, tests, pattern):
    return suite()


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
