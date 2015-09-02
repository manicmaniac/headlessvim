#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
.. note:: All the public interfaces of this module is exported to
          the top level module of ``headlessvim`` package.
"""

import tempfile
import pyte
from . import process
from . import arguments
from . import runtimepath


__all__ = ['Vim', 'open']


def open(**kwargs):
    """
    A factory function to open new ``Vim`` object.
    ``with`` statement can be used for this.
    """
    return Vim(**kwargs)


class Vim(object):
    """
    A class representing a headless *Vim*.
    Do not instantiate this directly, instead use ``open``.

    ``Vim`` object behaves as ``contextmanager``.

    :cvar default_args: the default launch argument of *Vim*
    :vartype default_args: string or list of string
    """
    default_args = '-N -i NONE -n -u NONE'

    def __init__(self,
                 executable='vim',
                 args=None,
                 env=None,
                 encoding='utf-8',
                 size=(80, 24),
                 timeout=0.25):
        """
        :param string executable: command name to execute *Vim*
        :param args: arguments to execute *Vim*
        :type args: None or string or list of string
        :param env: environment variables to execute *Vim*
        :type env: None or dict of (string, string)
        :param string encoding: internal encoding of *Vim*
        :param size: (lines, columns) of a screen connected to *Vim*
        :type size: (int, int)
        :param float timeout: seconds to wait I/O
        """
        parser = arguments.Parser(self.default_args)
        args = parser.parse(args)
        self._process = process.Process(executable, args, env)
        self._encoding = encoding
        self._screen = pyte.Screen(*size)
        self._stream = pyte.Stream()
        self._stream.attach(self._screen)
        self._timeout = timeout
        self._tempfile = tempfile.NamedTemporaryFile(mode='w+')
        self._runtimepath = None
        self.wait()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
        return True

    def __setattr__(self, name, value):
        if name == 'mode':
            self.set_mode(value)
        super(Vim, self).__setattr__(name, value)

    def close(self):
        """
        Disconnect and close *Vim*.
        """
        self._tempfile.close()
        self._process.terminate()
        if self._process.is_alive():
            self._process.kill()

    def is_alive(self):
        """
        Check if the background *Vim* process is alive.

        :return: True if the process is alive, else False
        :rtype: boolean
        """
        return self._process.is_alive()

    def display(self):
        """
        Shows the terminal screen connecting to *Vim*.

        Example:

        >>> with headlessvim.open(size=(64, 16)) as vim:
        ...     print(vim.display())
        ...
        ~
        ~                          VIM - Vi IMproved
        ~
        ~                           version 7.4.52
        ~                      by Bram Moolenaar et al.
        ~
        ~             Vim is open source and freely distributable
        ~
        ~                      Sponsor Vim development!
        ~           type  :help sponsor<Enter>    for information
        ~
        ~           type  :q<Enter>               to exit
        ~           type  :help<Enter>  or  <F1>  for on-line help
        ~           type  :help version7<Enter>   for version info
        ~
        ~

        :return: screen as a text
        :rtype: string
        """
        return '\n'.join(self.display_lines())

    def display_lines(self):
        """
        Shows the terminal screen splitted by newlines.

        Almost equals to ``self.display().splitlines()``

        :return: screen as a list of strings
        :rtype: list of string
        """
        return self._screen.display

    def send_keys(self, keys, wait=True):
        """
        Send a raw key sequence to *Vim*.

        .. note:: *Vim* style key sequence notation (like ``<Esc>``)
                  is not recognized.
                  Use escaped characters (like ``'\033'``) instead.

        Example:

        >>> with headlessvim.open() as vim:
        ...     vim.send_keys('ispam\033')
        ...     vim.display_lines()[0].strip()
        ...
        'spam'

        :param strgin keys: key sequence to send
        :param boolean wait: whether if wait a response
        """
        self._process.stdin.write(bytearray(keys, self._encoding))
        self._process.stdin.flush()
        if wait:
            self.wait()

    def wait(self, timeout=None):
        """
        Wait for response until timeout.
        If timeout is specified to None, ``self.timeout`` is used.

        :param float timeout: seconds to wait I/O
        """
        if timeout is None:
            timeout = self._timeout
        while self._process.check_readable(timeout):
            self._flush()

    def install_plugin(self, dir, entry_script=None):
        """
        Install *Vim* plugin.

        :param string dir: the root directory contains *Vim* script
        :param string entry_script: path to the initializing script
        """
        self.runtimepath.append(dir)
        if entry_script is not None:
            self.command('runtime! {0}'.format(entry_script), False)

    def command(self, command, capture=True):
        """
        Execute command on *Vim*.
        .. warning:: Do not use ``redir`` command if ``capture`` is ``True``.
                     It's already enabled for internal use.

        If ``capture`` argument is set ``False``,
        the command execution becomes slightly faster.

        Example:

        >>> with headlessvim.open() as vim:
        ...     vim.command('echo 0')
        ...
        '0'
        >>> with headlessvim.open() as vim:
        ...     vim.command('let g:spam = "ham"', False)
        ...     vim.echo('g:spam')
        ...
        'ham'

        :param string command: a command to execute
        :param boolean capture: ``True`` if command's output needs to be
                                captured, else ``False``
        :return: the output of the given command
        :rtype: string
        """
        if capture:
            self.command('redir! > {0}'.format(self._tempfile.name), False)
        self.set_mode('command')
        self.send_keys('{0}\n'.format(command))
        if capture:
            self.command('redir END', False)
            self._tempfile.seek(0)
            return self._tempfile.read().strip('\n')

    def echo(self, expr):
        """
        Execute ``:echo`` command on *Vim*.

        .. note:: The given string is passed to *Vim* as it is.
                  Make sure to quote bare words.

        Example:

        >>> with headlessvim.open() as vim:
        ...     vim.echo('0')
        ...
        '0'
        >>> with headlessvim.open() as vim:
        ...     vim.echo('"spam"')
        ...
        'spam'

        :param string expr: a expr to ``:echo``
        :return: the result of ``:echo`` command
        :rtype: string
        """
        return self.command('echo {0}'.format(expr))

    def set_mode(self, mode):
        """
        Set *Vim* mode to ``mode``.
        Supported modes:

        * ``normal``
        * ``insert``
        * ``command``
        * ``visual``
        * ``visual-block``


        This method behave as setter-only property.

        Example:

        >>> with headlessvim.open() as vim:
        ...     vim.set_mode('insert')
        ...     vim.mode = 'normal' # also accessible as property
        ...

        :param string mode: *Vim* mode to set
        :raises ValueError: if ``mode`` is not supported
        """
        keys = '\033\033'
        if mode == 'normal':
            pass
        elif mode == 'insert':
            keys += 'i'
        elif mode == 'command':
            keys += ':'
        elif mode == 'visual':
            keys += 'v'
        elif mode == 'visual-block':
            keys += 'V'
        else:
            raise ValueError('mode {0} is not supported'.format(mode))
        self.send_keys(keys)

    @property
    def executable(self):
        """
        :return: the absolute path to the process.
        :rtype: string
        """
        return self._process.executable

    @property
    def args(self):
        """
        :return: arguments for the process.
        :rtype: list of string
        """
        return self._process.args

    @property
    def encoding(self):
        """
        :return: internal encoding of *Vim*.
        :rtype: string
        """
        return self._encoding

    @property
    def screen_size(self):
        """
        :return: (lines, columns) tuple of a screen connected to *Vim*.
        :rtype: (int, int)
        """
        return self._swap(self._screen.size)

    @screen_size.setter
    def screen_size(self, size):
        """
        :param size: (lines, columns) tuple of a screen connected to *Vim*.
        :type size: (int, int)
        """
        if self.screen_size != size:
            self._screen.resize(*self._swap(size))

    @property
    def timeout(self):
        """
        :return: seconds to wait I/O.
        :rtype: float
        """
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """
        :param float timeout: seconds to wait I/O.
        """
        self._timeout = timeout

    @property
    def runtimepath(self):
        """
        :return: runtime path of *Vim*
        :rtype: runtimepath.RuntimePath
        """
        if self._runtimepath is None:
            self._runtimepath = runtimepath.RuntimePath(self)
        return self._runtimepath

    def _flush(self):
        buf = self._process.stdout.read()
        self._stream.feed(buf.decode(self._encoding))

    def _swap(self, size):
        return (size[1], size[0])
