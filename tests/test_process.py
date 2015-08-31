#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
import os
from headlessvim.process import Process


@pytest.fixture
def default_args(request):
    return '-N -i NONE -n -u NONE'


@pytest.fixture
def env(request):
    return dict(os.environ, LANG='C')


@pytest.fixture
def unterminated_process(request, default_args, env):
    return Process('vim', default_args, env)


@pytest.yield_fixture
def process(request, unterminated_process):
    process = unterminated_process
    yield process
    process.terminate()


def test_terminate(unterminated_process):
    process = unterminated_process
    assert process.is_alive()
    process.terminate()
    assert not process.is_alive()


def test_kill(unterminated_process):
    process = unterminated_process
    assert process.is_alive()
    process.kill()
    assert not process.is_alive()


def test_executable(process):
    assert 'vim' in process.executable
    assert os.path.isabs(process.executable)


def test_args(process, default_args):
    assert process.args == default_args


def test_stdin(process):
    assert hasattr(process.stdin, 'read')


def test_stdout(process):
    assert hasattr(process.stdout, 'write')
