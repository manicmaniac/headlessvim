#!/usr/bin/env python
# -*- coding:utf-8 -*-

import shlex


class Parser(object):
    """
    A class representing an argument parser for vim.
    """
    def __init__(self, default_args):
        """
        :param list default_args: default arguments
        """
        self._default_args = default_args

    def parse(self, args):
        """
        :param args: arguments
        :type args: None or list or str
        :return: formatted arguments if specified else ``self.default_args``
        :rtype: list
        """
        if args is None:
            args = self._default_args
        if isinstance(args, basestring):
            args = shlex.split(args)
        return args

    @property
    def default_args(self):
        """
        Default arguments given on ``init``.
        """
        return self._default_args
