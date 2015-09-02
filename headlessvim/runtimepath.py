#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
.. note:: This module is not designed to be used by user.
"""

import collections
import weakref


class RuntimePath(collections.MutableSequence):
    def __init__(self, vim):
        """
        :param vim: ``Vim`` object which owns this object.
        :type vim: Vim
        """
        self._ref = weakref.ref(vim)
        self._list = self.parse(vim.command('set runtimepath'))

    def __str__(self):
        return self.format(self._list)

    def __repr__(self):
        return self._list.__repr__()

    def __len__(self):
        return self._list.__len__()

    def __getitem__(self, key):
        return self._list.__getitem__(key)

    def __setitem__(self, key, value):
        self._list.__setitem__(key, value)
        self._sync()

    def __delitem__(self, key):
        self._list.__delitem__(key)
        self._sync()

    def insert(self, index, value):
        """
        Insert object before index.

        :param int index: index to insert in
        :param string value: path to insert
        """
        self._list.insert(index, value)
        self._sync()

    def format(self, list):
        """
        Format list to runtime path representation.

        :param list: list of paths to format
        :type list: list of string
        :return: *Vim* style runtime path string representation
        :rtype: string
        """
        values = ','.join(list)
        return 'runtimepath=' + values

    def parse(self, string):
        """
        Parse runtime path representation to list.

        :param string string: runtime path string
        :return: list of runtime paths
        :rtype: list of string
        """
        var, eq, values = string.strip().partition('=')
        assert var == 'runtimepath'
        assert eq == '='
        return values.split(',')

    def _sync(self):
        vim = self._ref()
        if vim:
            vim.command('set {0}'.format(str(self)), False)
