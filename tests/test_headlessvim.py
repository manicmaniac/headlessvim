#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
import os
from headlessvim.headlessvim import Vim, open


@pytest.yield_fixture
def vim(request):
    env = dict(os.environ, LANG='C')
    with open(env=env) as vim:
        yield vim


def test_open(vim):
    assert isinstance(vim, Vim)


def test_is_alive():
    env = dict(os.environ, LANG='C')
    vim = open(env=env)
    assert vim.is_alive()
    vim.close()
    assert not vim.is_alive()


def test_display(vim):
    display = vim.display()
    assert 'VIM - Vi IMproved' in display
    assert 'by Bram Moolenaar et al.' in display
    assert 'type  :q<Enter>' in display
    assert 'type  :help<Enter>' in display


def test_display_lines(vim):
    lines = vim.display_lines()
    assert all(len(line) == 80 for line in lines)
    assert any('VIM - Vi IMproved' in line for line in lines)
    assert lines[-1].strip() == ''


def test_display_command_window(vim):
    assert vim.display_command_window() == ''


def test_send_keys(vim):
    vim.send_keys('ispam\033')
    assert 'spam' in vim.display_lines()[0]


def test_command(vim):
    vim.command('echo "ham"')
    assert vim.display_command_window().rstrip() == 'ham'


def test_echo(vim):
    assert vim.echo('"egg"') == 'egg'


def test_executable(vim):
    assert 'vim' in vim.executable
    assert os.path.isabs(vim.executable)


def test_args(vim):
    assert '-u' in vim.args


def test_encoding(vim):
    assert vim.encoding.lower() == 'utf-8'


def test_size(vim):
    assert vim.screen_size == (80, 24)


def test_timeout(vim):
    assert vim.timeout == 0.1
