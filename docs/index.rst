.. headlessvim documentation master file, created by
   sphinx-quickstart on Wed Aug 26 02:46:42 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to headlessvim's documentation!
=======================================

.. code:: python

    >>> import headlessvim
    >>> with headlessvim.open() as vim:
    ...     vim.echo('"welcome!"') # make sure to quote bare words
    ...
    'welcome!'

Contents:

.. toctree::
    :maxdepth: 4

    install
    tutorial
    headlessvim
    license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
