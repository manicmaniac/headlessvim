#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
.. note:: This module is the public interface of ``headlessvim`` package.
          Import this module to start using ``headlessvim``.

Example:

>>> import headlessvim
>>> with headlessvim.open() as vim:
...     vim.echo('"spam"')
...
'spam'

.. autofunction:: open

.. autoclass:: Vim
    :members:
"""

from .headlessvim import * # flake8: noqa


__author__ = 'Ryosuke Ito'
__version__ = '0.0.4'
