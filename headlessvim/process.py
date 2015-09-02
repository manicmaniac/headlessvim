#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
.. note:: This module is not designed to be used by user.
"""

import contextlib
import distutils.spawn
import fcntl
import os
import pty
import select
import subprocess


class Process(object):
    """
    A class representing a background *Vim* process.
    """
    def __init__(self, executable, args, env):
        """
        :param str executable: command name to execute *Vim*
        :param args: arguments to execute *Vim*
        :type args: None or string or list of string
        :param env: environment variables to execute *Vim*
        :type env: None or dict of (string, string)
        """
        self._executable = distutils.spawn.find_executable(executable)
        self._args = args
        self._env = env
        self._open_process()

    def terminate(self):
        """
        Terminate this process.
        Use this method rather than ``self.kill``.
        """
        with self._close():
            self._process.terminate()

    def kill(self):
        """
        Kill this process.
        Use this only when the process seems to be hanging up.
        """
        with self._close():
            self._process.kill()

    def check_readable(self, timeout):
        """
        Poll ``self.stdout`` and return True if it is readable.

        :param float timeout: seconds to wait I/O
        :return: True if readable, else False
        :rtype: boolean
        """
        rlist, wlist, xlist = select.select([self._stdout], [], [], timeout)
        return bool(len(rlist))

    def is_alive(self):
        """
        Check if the process is alive.

        :return: True if the process is alive, else False
        :rtype: boolean
        """
        return self._process.poll() is None

    @property
    def executable(self):
        """
        :return: the absolute path to the process.
        :rtype: strIng
        """
        return self._executable

    @property
    def args(self):
        """
        :return: launch arguments of the process.
        :rtype: string or list of string
        """
        return self._args

    @property
    def stdin(self):
        """
        :return: file-like object representing the standard input
                 of the process
        :rtype: flie-like object
        """
        return self._stdin

    @property
    def stdout(self):
        """
        :return: non blocking file-like object
                 representing the standard output of the process
        :rtype: file-like object
        """
        return self._stdout

    def _open_process(self):
        master, slave = pty.openpty()
        self._process = subprocess.Popen(self._args,
                                         executable=self._executable,
                                         stdin=slave,
                                         stdout=slave,
                                         stderr=subprocess.STDOUT,
                                         env=self._env)
        self._open_stream(master)

    def _open_stream(self, fd):
        self._make_nonblock(fd)
        self._stdout = os.fdopen(fd, 'rb')
        self._stdin = os.fdopen(os.dup(fd), 'wb')

    def _close_stream(self):
        if not self._stdout.closed:
            self._stdout.close()
        if not self._stdin.closed:
            self._stdin.close()

    @contextlib.contextmanager
    def _close(self):
        self._close_stream()
        yield
        self._process.wait()

    def _make_nonblock(self, fd):
        fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
