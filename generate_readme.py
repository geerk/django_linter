from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os
import subprocess

from django_linter.checkers.settings import SettingsShecker
from django_linter.checkers.models import ModelsChecker
from django_linter.checkers.misc import MiscChecker
from django_linter.checkers.layout import LayoutChecker
from django_linter.checkers.forms import FormsChecker
from django_linter.checkers.views import ViewsChecker


def main():
    out = open('README.rst', 'w')
    print("""Django linter
=============

This is a simple extension for pylint that aims to check some common mistakes in django projects.

Contributions are welcome.

Only Python 2.7 supported for now.

Installation
------------

::

    pip install django_linter

Usage
-----
""", file=out)
    print('::', file=out)
    print('', file=out)
    usage = os.tmpfile()
    p = subprocess.Popen(
        ['python', '-m', 'django_linter.main', '-h'], stdout=usage)
    p.wait()
    usage.seek(0)
    for line in usage:
        if line != '\n':
            out.write('    ' + line.replace('main.py', 'django-linter'))
        else:
            out.write(line)
    print('', file=out)
    print('Implemented checks', file=out)
    print('------------------', file=out)
    print('', file=out)
    for checker in (SettingsShecker, ModelsChecker, FormsChecker, ViewsChecker,
                    LayoutChecker, MiscChecker):
        print('**%s:**' % checker.name.title(), file=out)
        print('', file=out)
        for k in sorted(checker.msgs.viewkeys()):
            print('- %s (%s): %s' % (k, checker.msgs[k][1], checker.msgs[k][2]),
                  file=out)
        print('', file=out)


if __name__ == '__main__':
    main()
