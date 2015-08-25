#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
import os
import time
from headlessvim.process import Process


@pytest.yield_fixture
def process(request):
    env = dict(os.environ, LANG='C')
    process = Process('vim', '-N -i NONE -n -u NONE', env)
    yield process
    process.terminate()


def test_terminate():
    env = dict(os.environ, LANG='C')
    process = Process('vim', '-N -i NONE -n -u NONE', env)
    assert process.is_alive()
    process.terminate()
    assert not process.is_alive()


def test_kill():
    env = dict(os.environ, LANG='C')
    process = Process('vim', '-N -i NONE -n -u NONE', env)
    assert process.is_alive()
    process.kill()
    assert not process.is_alive()


def test_check_readable(process):
    time.sleep(0.5)
    assert process.check_readable(0.1)
    process.stdout.read()
    assert not process.check_readable(0.1)


def test_executable(process):
    assert 'vim' in process.executable
    assert os.path.isabs(process.executable)


def test_args(process):
    assert process.args == '-N -i NONE -n -u NONE'


def test_stdin(process):
    assert hasattr(process.stdin, 'read')


def test_stdout(process):
    assert hasattr(process.stdin, 'write')
