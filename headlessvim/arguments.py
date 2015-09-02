#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
.. note:: This module is not designed to be used by user.
"""

import shlex
import six


class Parser(object):
    """
    A class to parse launch arguments for *Vim*.
    """
    def __init__(self, default_args):
        """
        :param default_args: default arguments
        :type default_args: string or list of string
        """
        self._default_args = default_args

    def parse(self, args):
        """
        :param args: arguments
        :type args: None or string or list of string
        :return: formatted arguments if specified else ``self.default_args``
        :rtype: list of string
        """
        if args is None:
            args = self._default_args
        if isinstance(args, six.string_types):
            args = shlex.split(args)
        return args

    @property
    def default_args(self):
        """
        :return: default arguments given on ``init``.
        :rtype: string or list of string
        """
        return self._default_args
