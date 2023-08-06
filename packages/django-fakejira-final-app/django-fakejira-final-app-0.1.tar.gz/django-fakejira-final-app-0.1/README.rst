fakejira-testing-app
====================

This is sample code used in the Real Python article [Writing an Installable Django App](???). The article describes how to take an app from an existing Django project and make it a stand-alone installable package avilable on PyPI.

Installable App
---------------

This app models a list of items on a receipt. Each item has a description and a cost. A receipt may reference multiple items.

This app can be installed and used in your django project by:

.. code-block:: bash

    $ pip install fakejira-testing-app


Edit your `settings.py` file to include `'fakejira1'` in the `INSTALLED_APPS`
listing.

.. code-block:: python

    INSTALLED_APPS = [
        ...

        'fakejira1',
    ]


Edit your project `urls.py` file to import the URLs:


.. code-block:: python

    url_patterns = [
        ...

        path('/', include('fakejira1.urls')),
    ]


Finally, add the models to your database:


.. code-block:: bash

    $ ./manage.py migrate fakejira1

