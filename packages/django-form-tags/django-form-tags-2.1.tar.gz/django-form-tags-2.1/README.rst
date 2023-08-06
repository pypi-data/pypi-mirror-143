Django form tags
================

.. image:: https://badge.fury.io/py/django-form-tags.png
    :target: https://badge.fury.io/py/django-form-tags

Django templatetags to easily render fieldholders, fieldwrappers and fields.


Installation
------------

.. code-block:: sh

    pip install django-form-tags


Usage
-----

.. code-block:: python

        INSTALLED_APPS = (
            # ...
            'form_tags',
            # ...
        )


.. code-block:: html

    {% load forms %}


Development
-------------

isort

.. code-block:: sh

    docker-compose run --rm --no-deps python isort [module/path] [options]

--------------

flake8

.. code-block:: sh

    docker-compose run --rm --no-deps python flake8 [module/path]


--------------

black

.. code-block:: sh

    docker-compose run --rm --no-deps python black [module/path]


--------------

pytest

.. code-block:: sh

    docker-compose run --rm --no-deps python coverage run ./runtests.py


Translations
------------
Updating translations

.. code:: sh

   docker-compose run --rm --no-deps manage makemessages -l nl --no-wrap --no-location --no-obsolete
   docker-compose run --rm --no-deps manage compilemessages
