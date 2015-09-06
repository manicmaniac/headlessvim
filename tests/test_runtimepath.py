#!/usr/bin/env python
# -*- coding:utf-8 -*-

import mock
import pytest

from headlessvim.runtimepath import RuntimePath


@pytest.fixture
def list(request):
    return ['~/.vim',
            '/var/lib/vim/addons',
            '/usr/share/vimfiles',
            '/usr/share/vim/vim74',
            '/usr/share/vim/vimfiles/after',
            '/var/lib/vim/addons/after',
            '~/.vim/after']


@pytest.fixture
def string(request):
    return '''runtimepath=~/.vim,
              /var/lib/vim/addons,
              /usr/share/vimfiles,
              /usr/share/vim/vim74,
              /usr/share/vim/vimfiles/after,
              /var/lib/vim/addons/after,
              ~/.vim/after'''.replace(' ', '').replace('\n', '')


@pytest.fixture
def vim(request, string):
    vim = mock.MagicMock()
    vim.command.return_value = string
    return vim


@pytest.fixture
def runtimepath(request, vim):
    return RuntimePath(vim)


@pytest.fixture
def path(request):
    return '/usr/local/share/vimfiles'


def test_str(runtimepath, string):
    assert str(runtimepath) == string


def test_repr(runtimepath, list):
    assert repr(runtimepath) == repr(list)


def test_del(runtimepath, string, vim):
    assert '~/.vim' in runtimepath
    del runtimepath[0]
    assert '~/.vim' not in runtimepath
    command = 'set {0}'.format(string.replace('~/.vim,', ''))
    vim.command.assert_called_with(command, False)
    assert vim.command.call_count == 2


@pytest.mark.parametrize('index', range(7))
def test_get_item(runtimepath, list, index):
    assert runtimepath[index] == list[index]


def test_set_item(runtimepath, path, string, vim):
    runtimepath[-1] = path
    assert runtimepath[-1] == path
    command = 'set {0}'.format(string.replace('~/.vim/after', path))
    vim.command.assert_called_with(command, False)
    assert vim.command.call_count == 2


def test_insert(runtimepath, path, string, vim):
    runtimepath.insert(0, path)
    assert runtimepath[0] == path
    command = 'set {0}'.format(
        string.replace('=~/.vim', '=' + path + ',~/.vim'))
    vim.command.assert_called_with(command, False)
    assert vim.command.call_count == 2


def test_append(runtimepath, path, string, vim):
    runtimepath.append(path)
    assert runtimepath[-1] == path
    command = 'set {0}'.format(string + ',' + path)
    vim.command.assert_called_with(command, False)
    assert vim.command.call_count == 2


def test_format(runtimepath, list, string):
    assert runtimepath.format(list) == string


def test_parse(runtimepath, list, string):
    assert runtimepath.parse(string) == list
