headlessvim
===========

.. image:: https://img.shields.io/travis/manicmaniac/headlessvim.svg
    :target: https://travis-ci.org/manicmaniac/headlessvim

.. image:: https://img.shields.io/coveralls/manicmaniac/headlessvim.svg
    :target: https://coveralls.io/github/manicmaniac/headlessvim?branch=master

.. image:: https://img.shields.io/codeclimate/github/manicmaniac/headlessvim.svg
    :target: https://codeclimate.com/github/manicmaniac/headlessvim
    :alt: Code Climate

.. image:: https://img.shields.io/pypi/v/headlessvim.svg
    :target: https://pypi.python.org/pypi/headlessvim
    :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/headlessvim.svg
    :target: https://pypi.python.org/pypi/headlessvim
    :alt: Python Versions

Introduction
------------

``headlessvim`` makes Vim programmable to support developping Vim plugins.

The most distinctive characteristic is,
``headlessvim`` NEVER needs ``+clientserver`` feature.

Install
-------

Using ``pip`` (recommended)

.. code:: sh

    pip install headlessvim

The good old ``setup.py``

.. code:: sh

    python setup.py install

Usage
-----

A simple example is here:

.. code:: python

    >>> import headlessvim
    >>> with headlessvim.open() as vim:
    ...    vim.echo('"spam"') # make sure to quote bare words
    ...
    'spam'
    >>> import os
    >>> env = dict(os.environ, LANG='C')
    >>> with headlessvim.open(executable='/usr/bin/vim', args='-N -u /etc/vim/vimrc', env=env):
    ...    vim.send_keys('iham\033')
    ...    vim.display_lines()[0].strip()
    ...
    'ham'

Integrating to ``unittest``:

.. code:: python

    import unittest
    import headlessvim

    class TestVimPlugin(unittest.TestCase):
        def setUp(self):
            self.vim = headlessvim.open()

        def tearDown(self):
            self.vim.close()

        def testSomeFeature(self):
            res = self.vim.echo('"ham egg"')
            self.assertEqual(res, 'ham egg')

Documentation
-------------

See `the online document <http://pythonhosted.org/headlessvim/>`_ for more information.

Testing
-------

Execute:

.. code:: sh

    python setup.py test


License
-------

The MIT License.

See `LICENSE.txt <LICENSE.txt>`_ for more information.
