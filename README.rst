Django linter
=============

This is a simple extension for pylint that is aim to check some common mistakes in django projects.

Contributions are welcome.

Only Python 2.7 supported for now.

Installation
------------

    pip install django_linter

Usage
-----

    usage: django-linter [-h] TARGET [TARGET ...]

    Simple extension for pylint to check django projects for common mistakes.

    positional arguments:
      TARGET      python package or module

    optional arguments:
      -h, --help  show this help message and exit

Implemented checks
------------------

**Settings:**

- E5002 (empty-setting): Used when setting is empty value.
- E5001 (required-setting-missed): Used when required setting missed in settings file.

**Models:**

- W5104 (related-field-named-with-id): Used when related field is named with _id suffix
- W5105 (unicode-method-absent): Used when model has no unicode method.
- W5106 (unicode-method-return): Used when unicode method does not return unicode.
- W5101 (nullable-text-field): Used when text field has null=True.
- W5102 (float-money-field): Used when money related field uses FloatField.
- W5103 (naive-datetime-used): Used when there is datetime.now is used.

**Misc:**

- W5201 (print-used): Used when there is print statement or function

**Layout:**

- W5302 (admin-layout): Used when admin class definition is not in adin module.
- W5301 (forms-layout): Used when form class definition is not in forms module.
