#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tempfile
import pyte
from . import process
from . import arguments
from . import runtimepath


__all__ = ['Vim', 'open']


def open(**kwargs):
    """
    A factory function to open new Vim object.
    ``with`` statement can be used for this.
    """
    return Vim(**kwargs)


class Vim(object):
    """
    A class representing a headless Vim.
    Do not instantiate this directly, instead use ``open``.
    """
    default_args = '-N -i NONE -n -u NONE'

    def __init__(self,
                 executable='vim',
                 args=None,
                 env=None,
                 encoding='utf-8',
                 size=(80, 24),
                 timeout=0.1):
        """
        :param str executable: command name to execute Vim
        :param args: arguments to execute Vim
        :type args: None or list or str
        :param env: environment variables to execute Vim
        :type env: None or dict
        :param str encoding: internal encoding of Vim
        :param tuple size: (lines, columns) of a screen connected to Vim
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
        Disconnect and close Vim.
        """
        self._tempfile.close()
        self._process.terminate()
        if self._process.is_alive():
            self._process.kill()

    def is_alive(self):
        """
        Check if the background Vim process is alive.

        :return: True if the process is alive, else False
        """
        return self._process.is_alive()

    def display(self):
        """
        Shows the terminal screen connecting to Vim.

        :return: screen as a text
        :rtype: str
        """
        return '\n'.join(self.display_lines())

    def display_lines(self):
        """
        Shows the terminal screen splitted by newlines.

        :return: screen as a list of strings
        :rtype: list
        """
        return self._screen.display

    def send_keys(self, keys, wait=True):
        """
        Send a raw key sequence to Vim.

        :param str keys: key sequence to send
        :param bool wait: whether if wait a response
        """
        self._process.stdin.write(bytearray(keys, self._encoding))
        self._process.stdin.flush()
        if wait:
            self.wait()

    def wait(self, timeout=None):
        """
        Wait for response until timeout.

        :param float timeout: seconds to wait I/O
        """
        if timeout is None:
            timeout = self._timeout
        while self._process.check_readable(timeout):
            self._flush()

    def install_plugin(self, dir, entry_script=None):
        """
        Install Vim plugin.

        :param str dir: the root directory contains Vim script
        :param str entry_script: path to the initializing script
        """
        self.runtimepath.append(dir)
        if entry_script is not None:
            self.command('runtime! {0}'.format(entry_script), False)

    def command(self, command, capture=True):
        """
        Execute command on Vim.
        Do not use ``redir`` command if ``capture`` is ``True``.
        It's already enabled for internal use.

        :param str command: a command to execute
        :param bool capture: ``True`` if command's output needs to be
        captured, else ``False``
        :return: the output of command
        :rtype: str
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
        Execute ``:echo`` command on Vim.

        :param str expr: a expr to ``:echo``
        :return: the result of ``:echo`` command
        :rtype: str
        """
        return self.command('echo {0}'.format(expr))

    def set_mode(self, mode):
        """
        Set Vim mode to ``mode``.
        Supported modes: ``normal``, ``insert``, ``command``,
        ``visual``, ``visual-block``
        Raises ValueError if ``mode`` is not supported.

        :param str mode: Vim mode to set
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
        The absolute path to the process.
        """
        return self._process.executable

    @property
    def args(self):
        """
        Arguments for the process.
        """
        return self._process.args

    @property
    def encoding(self):
        """
        Internal encoding of Vim.
        """
        return self._encoding

    @property
    def screen_size(self):
        """
        (lines, columns) tuple of a screen connected to Vim.
        """
        # somehow pyte swaps `size` tuple
        return (self._screen.size[1], self._screen.size[0])

    @screen_size.setter
    def screen_size(self, size):
        """
        (lines, columns) tuple of a screen connected to Vim.
        """
        self._screen.resize(*size)

    @property
    def timeout(self):
        """
        Seconds to wait I/O.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """
        Seconds to wait I/O.
        """
        self._timeout = timeout

    @property
    def runtimepath(self):
        if self._runtimepath is None:
            self._runtimepath = runtimepath.RuntimePath(self)
        return self._runtimepath

    def _flush(self):
        buf = self._process.stdout.read()
        self._stream.feed(buf.decode(self._encoding))
