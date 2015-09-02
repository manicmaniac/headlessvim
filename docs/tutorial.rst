Tutorial
========

Basic Usage
-----------

Firstly, import module.
*headlessvim* module has some submodules for internal use.
Only the top module is designed to import by user.

.. code:: python

    >>> import headlessvim

.. warning::

    **DO NOT** import by ``from headlessvim import *``.
    *headlessvim* module has the function named ``open``.
    So it hides built-in ``open`` function.

Secondly, open the background *Vim* process.
``open`` is the only entry point to open *Vim*.

.. code:: python

    >>> vim = headlessvim.open()

``open`` returns ``Vim`` object which is the interface to
the background *Vim* process.

``open`` takes some arguments which are passed to the constructor of ``Vim``.

.. autofunction:: headlessvim.open

.. autoclass:: headlessvim.Vim

.. note::
    Make sure not instantiate ``Vim`` by its constructor.
    It's like the relationship between built-in ``file`` and ``open``.

Let it say something:

.. code:: python

    >>> vim.echo('"spam"') # make sure to quote bare words
    'spam'

Yes, ``vim.echo`` actually invokes ``:echo`` command of the background *Vim*,
so you should quote bare words twice.

To know what is possible, see :py:class:`headlessvim.headlessvim.Vim`.

Generally, something which has been opened should be closed
when the manipulation has been finished.
``Vim`` is not the exception.

.. code:: python

    >>> vim.close()

Of course you can use ``with`` statement to ensure closing ``Vim``.
It is recommended.

.. code:: python

    >>> with headlessvim.open() as vim:
    ...     vim.echo('"spam"')
    ...
    'spam'

More complex example:

.. code:: python

    >>> import headlessvim
    >>> with headlessvim.open() as vim:
    ...    vim.echo('"spam"') # make sure to quote bare words
    ...
    'spam'
    >>> import os
    >>> env = dict(os.environ, LANG='C')
    >>> with headlessvim.open(executable='/usr/bin/vim', args='-N -u /etc/vim/vimrc', env=env): # doctest: +SKIP
    ...    vim.send_keys('iham\033')
    ...    vim.display_lines()[0].strip()
    ...
    'ham'


Unit Test Integration
---------------------

*headlessvim* is useful for testing vim plugins.

An example for standard *PyUnit*:

.. code:: python

    import unittest
    import headlessvim


    class TestVimPlugin(unittest.TestCase):
        def setUp(self):
            self.vim = headlessvim.open()
            self.vim.install_plugin('fixtures/spam', 'plugin/spam.vim')

        def tearDown(self):
            self.vim.close()

        def testSomeFeature(self):
            res = self.vim.echo('"ham egg"')
            self.assertEqual(res, 'ham egg')

More example for `pytest <http://pytest.org>`_:

.. code:: python

    import os
    import pytest
    import headlessvim


    @pytest.fixture
    def env(request):
        return dict(os.environ, LANG='C')


    @pytest.yield_fixture
    def vim(request, env):
        with headlessvim.open(args='-N -u /etc/vim/vimrc', env=env) as vim:
            vim.install_plugin('fixtures/spam', 'plugin/spam.vim')
            yield vim


    def test_spam(vim):
        assert vim.echo('"spam"') == 'spam'
