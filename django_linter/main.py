from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from argparse import ArgumentParser


from pylint import lint, reporters

from . import register


def main():
    arg_parser = ArgumentParser(
        description='Simple extension for pylint to check django projects for '
                    'common mistakes.')
    arg_parser.add_argument('targets', metavar='TARGET', nargs='+',
                            help='python package or module')

    args = arg_parser.parse_args()

    linter = lint.PyLinter()
    reporters.initialize(linter)
    linter._load_reporter()
    register(linter)

    with lint.fix_import_path(args.targets):
        linter.check(args.targets)

    return linter.msg_status


if __name__ == '__main__':
    main()
