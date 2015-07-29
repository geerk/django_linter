#!/usr/bin/env python

from setuptools import setup

setup(
    name='django_linter',
    version='0.3',
    packages=('django_linter', 'django_linter.checkers'),
    description='Linter for django projects',
    long_description=open('README.rst').read(),
    author='Timofey Trukhanov',
    author_email='timofey.trukhanov@gmail.com',
    license='MIT',
    url='https://github.com/geerk/django_linter',
    install_requires=('pylint',),
    entry_points={
        'console_scripts': ['django-linter = django_linter.main:main']},
    classifiers = (
        'Development Status :: 4 - Beta',
        'Classifier: Framework :: Django :: 1.4',
        'Classifier: Framework :: Django :: 1.5',
        'Classifier: Framework :: Django :: 1.6',
        'Classifier: Framework :: Django :: 1.7',
        'Classifier: Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent'))
