monica
======

|image0|

🍴 monica is a command line chef that brings you tasty food

Demo
----

|image1|

Features
--------

-  Written in Python
-  Uses the Zomato API, so works in 23 countries.
-  Works on Linux, Windows and Mac.

Installation
------------

1: `PIP`_
~~~~~~~~~

.. code:: bash

    $ pip install monica

2: From Source
~~~~~~~~~~~~~~

.. code:: bash

    $ git clone https://github.com/Zephrys/monica
    $ cd monica/
    $ python setup.py install

Usage
-----

Search for a restaurant
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ monica search Good Chinese Food

Get surprised by something random in your budget
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ monica surprise

Get restaurants that support a specific cuisine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ monica cuisine Indian

Or to get a list of cuisines

.. code:: bash

    $ monica cuisine list

Get a list of restaurants in your budget.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ monica budget 500

Get details of a particular restaurant by id
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ monica restaurant 310543

Get reviews of a restaruant by id
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ monica reviews 310543

Reconfigure Monica
~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ monica configure

Help
~~~~

.. code:: bash

    $ monica --help

Contributing
------------

Use the `issue tracker`_ to file bugs or push new features.

License
-------

Open sourced under the **MIT License**

.. _PIP: 
.. _issue tracker: https://github.com/Zephrys/monica

.. |image0| image:: http://i.imgur.com/mfJa6zi.jpg?1
.. |image1| image:: http://i.imgur.com/D4iLyJw.gif?1