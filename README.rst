Django linter
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

- E5001 (required-setting-missed): Used when required setting missed in settings file.
- E5002 (empty-setting): Used when setting is empty value.
- W5001 (improper-settings-import): Used when settings is not imported from django.conf

**Models:**

- W5101 (nullable-text-field): Used when text field has null=True.
- W5102 (float-money-field): Used when money related field uses FloatField.
- W5103 (naive-datetime-used): Used when there is datetime.now is used.
- W5104 (related-field-named-with-id): Used when related field is named with _id suffix
- W5105 (unicode-method-absent): Used when model has no unicode method.
- W5106 (unicode-method-return): Used when unicode method does not return unicode.
- W5107 (model-field-redefinition): Used when there are more than one model field with the same name.
- W5108 (get-absolute-url-without-reverse): Used when get_absolute_url method is defined without using reverse function.

**Forms:**

- W5401 (form-field-redefinition): Used when there are more than one form field with the same name.

**Views:**

- W5501 (is-authenticated-not-called): Used when is_authenticated method is not called
- W5502 (objects-get-without-doesnotexist): Used when Model.objects.get is used without enclosing it in try-except block to catch DoesNotExist exception.
- W5503 (fetching-db-objects-len): Used when there is db query that fetches objects from database only to check the number of returned objects.
- W5504 (raw-get-post-access): Used when request.GET or request.POST dicts is accessed directly, it is better to use forms.

**Layout:**

- W5301 (forms-layout): Used when form class definition is not in forms module.
- W5302 (admin-layout): Used when admin class definition is not in admin module.

**Misc:**

- W5201 (print-used): Used when there is print statement or function

