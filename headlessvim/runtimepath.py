#!/usr/bin/env python
# -*- coding:utf-8 -*-

import collections
import weakref


class RuntimePath(collections.MutableSequence):
    def __init__(self, vim):
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
        self._list.insert(index, value)
        self._sync()

    def format(self, list):
        values = ','.join(list)
        return 'runtimepath=' + values

    def parse(self, string):
        var, eq, values = string.strip().partition('=')
        assert var == 'runtimepath'
        assert eq == '='
        return values.split(',')

    def _sync(self):
        vim = self._ref()
        if vim:
            vim.command('set {0}'.format(str(self)), capture=False)
