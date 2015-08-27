###########
headlessvim
###########

.. image:: https://travis-ci.org/manicmaniac/headlessvim.svg
    :target: https://travis-ci.org/manicmaniac/headlessvim

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

The good old ``setup.py``::

    python setup.py install

========
Examples
========

A simple example is here::

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

Integrating to ``unittest``::

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

Execute::

    python setup.py test


=======
License
=======

The MIT License.

See `LICENSE.txt <LICENSE.txt>`_ for more information.
