import unittest
import sys
import re
import os

from pylint.testutils import (make_tests, LintTestUsingModule, LintTestUsingFile,
    LintTestUpdate, cb_test_gen, linter, test_reporter)


def suite():
    input_dir = os.path.join(os.path.dirname(__file__), 'input')
    msg_dir = os.path.join(os.path.dirname(__file__), 'messages')
    linter.load_plugin_modules(['django_linter'])
    linter.global_set_option('required-attributes', ())
    return unittest.TestSuite([
        unittest.makeSuite(test, suiteClass=unittest.TestSuite)
        for test in make_tests(input_dir, msg_dir, None, [cb_test_gen(LintTestUsingFile)])])


def load_tests(loader, tests, pattern):
    return suite()


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
