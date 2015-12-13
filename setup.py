#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django_linter',
    version='0.7',
    packages=find_packages(exclude=['tests*']),
    description='Linter for django projects',
    long_description=open('README.rst').read(),
    author='Timofey Trukhanov',
    author_email='timofey.trukhanov@gmail.com',
    license='MIT',
    url='https://github.com/geerk/django_linter',
    install_requires=('pylint==1.5.1',),
    entry_points={
        'console_scripts': ['django-linter = django_linter.main:main']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent'])
