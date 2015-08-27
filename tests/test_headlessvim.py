#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import os
from headlessvim.headlessvim import Vim, open


class TestHeadlessVim(unittest.TestCase):
    def setUp(self):
        env = dict(os.environ, LANG='C')
        self.vim = open(env=env)
        self.skip_close = False

    def tearDown(self):
        if not self.skip_close:
            self.vim.close()

    def testOpen(self):
        self.assertTrue(isinstance(self.vim, Vim))

    def testIsAlive(self):
        self.skip_close = True
        self.assertTrue(self.vim.is_alive())
        self.vim.close()
        self.assertFalse(self.vim.is_alive())

    def testDisplay(self):
        display = self.vim.display()
        self.assertTrue('VIM - Vi IMproved' in display)
        self.assertTrue('by Bram Moolenaar et al.' in display)
        self.assertTrue('type  :q<Enter>' in display)
        self.assertTrue('type  :help<Enter>' in display)

    def testDisplayLines(self):
        lines = self.vim.display_lines()
        self.assertTrue(all(len(line) == 80 for line in lines))
        self.assertTrue(any('VIM - Vi IMproved' in line for line in lines))
        self.assertEqual(lines[-1].strip(), '')

    def testDisplayCommandWindow(self):
        self.assertEqual(self.vim.display_command_window(), '')

    def testSendKeys(self):
        self.vim.send_keys('ispam\033')
        self.assertTrue('spam' in self.vim.display_lines()[0])

    def testCommand(self):
        self.vim.command('echo "ham"')
        self.assertEqual(self.vim.display_command_window().rstrip(), 'ham')

    def testEcho(self):
        self.assertTrue(self.vim.echo('"egg"'), 'egg')

    def testExecutable(self):
        self.assertTrue('vim' in self.vim.executable)
        self.assertTrue(os.path.isabs(self.vim.executable))

    def testArgs(self):
        self.assertTrue('-u' in self.vim.args)

    def testEncoding(self):
        self.assertEqual(self.vim.encoding.lower(), 'utf-8')

    def testSize(self):
        self.assertEqual(self.vim.screen_size, (80, 24))

    def testTimeout(self):
        self.assertEqual(self.vim.timeout, 0.1)
