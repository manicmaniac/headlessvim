#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock
from headlessvim.runtimepath import RuntimePath


class TestRuntimePath(unittest.TestCase):
    def setUp(self):
        self.string = '''runtimepath=~/.vim,
                         /var/lib/vim/addons,
                         /usr/share/vimfiles,
                         /usr/share/vim/vim74,
                         /usr/share/vim/vimfiles/after,
                         /var/lib/vim/addons/after,
                         ~/.vim/after'''.replace(' ', '').replace('\n', '')
        self.list = [
            '~/.vim',
            '/var/lib/vim/addons',
            '/usr/share/vimfiles',
            '/usr/share/vim/vim74',
            '/usr/share/vim/vimfiles/after',
            '/var/lib/vim/addons/after',
            '~/.vim/after',
        ]
        self.len = 7
        self.vim = mock.MagicMock()
        self.vim.command.return_value = self.string
        self.runtimepath = RuntimePath(self.vim)

    def testStr(self):
        self.assertEqual(str(self.runtimepath), self.string)

    def testRepr(self):
        self.assertEqual(repr(self.runtimepath), repr(self.list))

    def testDel(self):
        self.assertTrue('~/.vim' in self.runtimepath)
        del self.runtimepath[0]
        self.assertFalse('~/.vim' in self.runtimepath)
        command = 'set {0}'.format(self.string.replace('~/.vim,', ''))
        self.vim.command.assert_called_with(command, capture=False)
        self.assertEqual(self.vim.command.call_count, 2)

    def testLen(self):
        self.assertEqual(len(self.runtimepath), self.len)

    def testGetItem(self):
        self.assertEqual(self.runtimepath[0], self.list[0])
        self.assertEqual(self.runtimepath[1], self.list[1])
        self.assertEqual(self.runtimepath[-1], self.list[-1])

    def testSetItem(self):
        path = '/usr/local/share/vimfiles'
        self.runtimepath[-1] = path
        self.assertEqual(self.runtimepath[-1], path)
        command = 'set {0}'.format(self.string.replace('~/.vim/after', path))
        self.vim.command.assert_called_with(command, capture=False)
        self.assertEqual(self.vim.command.call_count, 2)

    def testInsert(self):
        path = '/usr/local/share/vimfiles'
        self.runtimepath.insert(0, path)
        self.assertEqual(self.runtimepath[0], path)
        command = 'set {0}'.format(self.string.replace('=~/.vim', '=' + path + ',~/.vim'))
        self.vim.command.assert_called_with(command, capture=False)
        self.assertEqual(self.vim.command.call_count, 2)

    def testAppend(self):
        path = '/usr/local/share/vimfiles'
        self.runtimepath.append(path)
        self.assertEqual(self.runtimepath[-1], path)
        command = 'set {0}'.format(self.string + ',' + path)
        self.vim.command.assert_called_with(command, capture=False)
        self.assertEqual(self.vim.command.call_count, 2)

    def testFormat(self):
        self.assertEqual(self.runtimepath.format(self.list), self.string)

    def testParse(self):
        self.assertEqual(self.runtimepath.parse(self.string), self.list)
