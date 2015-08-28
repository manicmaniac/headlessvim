###########
headlessvim
###########

.. image:: https://travis-ci.org/manicmaniac/headlessvim.svg
    :target: https://travis-ci.org/manicmaniac/headlessvim

.. image:: https://coveralls.io/repos/manicmaniac/headlessvim/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/manicmaniac/headlessvim?branch=master

.. image:: https://codeclimate.com/github/manicmaniac/headlessvim/badges/gpa.svg
    :target: https://codeclimate.com/github/manicmaniac/headlessvim
    :alt: Code Climate

============
Introduction
============

``headlessvim`` makes Vim programmable to support developping Vim plugins.

The most distinctive characteristic is,
``headlessvim`` NEVER needs ``+clientserver`` feature.

Also, ``headlessvim`` is fully compatible among Python 2.6, 2.7, 3.2, 3.3, 3.4.

=======
Install
=======

The good old ``setup.py``

.. code:: sh

    python setup.py install

========
Examples
========

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

=======
Testing
=======

The unit test requires ``pytest`` module.

Execute:

.. code:: sh

    python setup.py test


=======
License
=======

The MIT License.

See `LICENSE.txt <LICENSE.txt>`_ for more information.
