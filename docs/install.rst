Install
=======

External Dependencies
---------------------

Only *Vim* is required.

.. code:: sh

    vim --version

.. note::

    *headlessvim* does **NOT** depend on *Vim*'s *+clientserver* feature.
    Also, *+python* and *+python3* are **NOT** required.

.. note::

    If *Vim* is not in the ``$PATH`` environment variable,
    you can indicate which *Vim* to use in the code (mentioned later).


Python Versions
---------------

*headlessvim* is tested on *Python* s below:

* *Python 2.6*
* *Python 2.7*
* *Python 3.2*
* *Python 3.3*
* *Python 3.4*


Installation
------------

The easy way (using package manager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using *pip* (recommended)

.. code:: sh

    pip install headlessvim


The hard way (build from source)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Checkout from the repository, then the good old *setup.py*

.. code:: sh

    git clone https://github.com/manicmaniac/headlessvim.git
    cd headlessvim
    python setup.py install


Windows Support
---------------

Sorry, *Windows* is not supported currently.
