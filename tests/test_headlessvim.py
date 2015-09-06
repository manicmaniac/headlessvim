#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

import mock
import pytest

from headlessvim import Vim, open


@pytest.fixture
def env(request):
    return dict(os.environ, LANG='C')


@pytest.fixture
def unterminated_vim(request, env):
    return open(env=env)


@pytest.yield_fixture
def vim(request, unterminated_vim):
    vim = unterminated_vim
    yield vim
    vim.close()


@pytest.fixture
def fixtures(request):
    here = os.path.dirname(__file__)
    return os.path.join(here, 'fixtures')


@pytest.fixture
def plugin_dir(request, fixtures):
    return os.path.join(fixtures, 'spam')


@pytest.fixture
def plugin_entry_script(request):
    return 'plugin/spam.vim'


@pytest.fixture
def zombie_vim(request, unterminated_vim):
    vim = unterminated_vim
    vim.close()
    vim._process = mock.MagicMock()
    vim._process.is_alive.return_value = True
    return vim


def test_open(vim):
    assert isinstance(vim, Vim)


def test_close_zombie(zombie_vim):
    vim = zombie_vim
    vim.close()
    vim._process.terminate.assert_called_once_with()
    vim._process.kill.assert_called_once_with()


def test_del(zombie_vim):
    vim = zombie_vim
    vim.__del__()
    vim._process.terminate.assert_called_once_with()
    vim._process.kill.assert_called_once_with()


def test_context_manager():
    with open() as vim:
        assert isinstance(vim, Vim)
        assert vim.is_alive()
    assert not vim.is_alive()


def test_is_alive(unterminated_vim):
    vim = unterminated_vim
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


def test_send_keys(vim):
    vim.send_keys('ispam\033')
    assert 'spam' in vim.display_lines()[0]


def test_install_plugin(vim, plugin_dir, plugin_entry_script):
    vim.install_plugin(plugin_dir, plugin_entry_script)
    assert plugin_dir in vim.runtimepath
    assert vim.command('Spam') == 'spam'


def test_command(vim):
    message = 'spam'
    assert vim.command('echo "{0}"'.format(message)) == message


def test_echo(vim):
    message = 'spam'
    assert vim.echo('"{0}"'.format(message)) == message


def test_set_mode(vim):
    vim.set_mode('insert')
    vim.send_keys('spam')
    vim.set_mode('normal')
    assert vim.display_lines()[0].strip() == 'spam'
    vim.set_mode('visual')
    vim.send_keys('0yP')
    assert vim.display_lines()[0].strip() == 'spamspam'
    vim.send_keys('yyp')
    vim.set_mode('visual-block')
    vim.send_keys('kIspam')
    assert vim.display_lines()[0].strip() == 'spamspamspam'


def test_set_mode_invalid(vim):
    with pytest.raises(ValueError):
        vim.set_mode('invalid-mode')


def test_set_mode_setter(vim):
    vim.mode = 'insert'
    vim.send_keys('spam')
    vim.mode = 'normal'
    assert vim.display_lines()[0].strip() == 'spam'


def test_executable(vim):
    assert 'vim' in vim.executable
    assert os.path.isabs(vim.executable)


def test_args(vim):
    assert '-u' in vim.args


def test_encoding(vim):
    assert vim.encoding.lower() == 'utf-8'


def test_screen_size(vim):
    assert vim.screen_size == (80, 24)


def test_screen_size_setter(vim):
    screen_size = (120, 32)
    vim.screen_size = screen_size
    assert vim.screen_size == screen_size
    assert all(len(line) == screen_size[0] for line in vim.display_lines())


def test_timeout(vim):
    assert 0 < vim.timeout < 1


def test_timeout_setter(vim):
    vim.timeout = 10
    assert vim.timeout == 10
