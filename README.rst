Django linter
=============

.. image:: https://travis-ci.org/geerk/django_linter.svg?branch=master
    :target: https://travis-ci.org/geerk/django_linter

This is a simple extension for pylint that aims to check some common mistakes in django projects.

Contributions are welcome.

Installation
------------

::

    pip install django_linter

Usage
-----

It can be used as a plugin or standalone script. To use it as a plugin it should be installed first, then run with pylint:

::

    pylint --load-plugins=django_linter TARGET

To use it as a standalone script:


::

    usage: django-linter [-h] TARGET [TARGET ...]

    Simple extension for pylint to check django projects for common mistakes.

    positional arguments:
      TARGET      python package or module

    optional arguments:
      -h, --help  show this help message and exit

Implemented checks
------------------

**Settings:**

- E5221 (required-setting-missed): Used when required setting missed in settings file.
- E5222 (empty-setting): Used when setting is empty value.
- W5221 (improper-settings-import): Used when settings is not imported from django.conf

**Models:**

- W5241 (nullable-text-field): Used when text field has null=True.
- W5242 (float-money-field): Used when money related field uses FloatField.
- W5243 (naive-datetime-used): Used when there is datetime.now is used.
- W5244 (related-field-named-with-id): Used when related field is named with _id suffix
- W5245 (unicode-method-absent): Used when model has no unicode method.
- W5246 (unicode-method-return): Used when unicode method does not return unicode.
- W5247 (model-field-redefinition): Used when there are more than one model field with the same name.
- W5248 (get-absolute-url-without-reverse): Used when get_absolute_url method is defined without using reverse function.

**Forms:**

- W5211 (form-field-redefinition): Used when there are more than one form field with the same name.

**Views:**

- W5231 (is-authenticated-not-called): Used when is_authenticated method is not called
- W5232 (objects-get-without-doesnotexist): Used when Model.objects.get is used without enclosing it in try-except block to catch DoesNotExist exception.
- W5233 (fetching-db-objects-len): Used when there is db query that fetches objects from database only to check the number of returned objects.
- W5234 (raw-get-post-access): Used when request.GET or request.POST dicts is accessed directly, it is better to use forms.

**Layout:**

- W5201 (forms-layout): Used when form class definition is not in forms module.
- W5202 (admin-layout): Used when admin class definition is not in admin module.

**Misc:**

- W5251 (print-used): Used when there is print statement or function

Implemented suppressers
-----------------------

- "Meta" classes
- urlpatterns
- logger

