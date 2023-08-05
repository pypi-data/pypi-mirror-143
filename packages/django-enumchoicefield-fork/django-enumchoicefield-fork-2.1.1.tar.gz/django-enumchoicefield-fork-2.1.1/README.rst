=================================
Django EnumChoiceField - The fork
=================================


A Django model field for native Python Enums.

Warning
=======
TL;DR - Think twice before using this package.
This is an ad hoc fork of the unmaintained `Django EnumChoiceField <https://pypi.org/project/django-enumchoicefield/>`_ that can be used by projects that are dependant on the said package.
For new projects (or projects that look for a better way to handle enums) you are strongly advised to check out the maintained `Django EnumFields <https://pypi.org/project/django-enumfields/>`_.

A quick how-to
==============
.. code:: python

    from enumchoicefield import ChoiceEnum, EnumChoiceField

    class Fruit(ChoiceEnum):
        apple = "Apple"
        banana = "Banana"
        orange = "Orange"

    class Profile(models.Model):
        name = models.CharField(max_length=100)
        favourite_fruit = EnumChoiceField(Fruit, default=Fruit.banana)

Documentation
=============

See `Django EnumChoiceField on ReadTheDocs <https://django-enumchoicefield.readthedocs.org/en/latest/>`_.

Testing
=======

To run the tests:

.. code:: sh

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements-dev.txt
    $ tox
