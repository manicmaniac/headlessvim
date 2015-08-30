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
        fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        self.plugin_dir = os.path.join(
            fixtures_dir,
            'spam'
        )
        assert os.path.isdir(self.plugin_dir)
        self.plugin_entry_script = 'plugin/spam.vim'

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

    def testSendKeys(self):
        self.vim.send_keys('ispam\033')
        self.assertTrue('spam' in self.vim.display_lines()[0])

    def testInstallPlugin(self):
        self.vim.install_plugin(self.plugin_dir, self.plugin_entry_script)
        self.assertTrue(self.plugin_dir in self.vim.runtimepath)
        self.assertEqual(self.vim.command('Spam'), 'spam')

    def testCommand(self):
        self.assertEqual(self.vim.command('echo "ham"'), 'ham')
        self.assertEqual(self.vim.command('echo "egg"'), 'egg')

    def testEcho(self):
        self.assertEqual(self.vim.echo('"ham"'), 'ham')
        self.assertEqual(self.vim.echo('"egg"'), 'egg')

    def testSetMode(self):
        self.vim.set_mode('insert')
        self.vim.send_keys('spam')
        self.vim.set_mode('normal')
        self.assertEqual(self.vim.display_lines()[0].strip(), 'spam')

    def testSetModeInvalid(self):
        self.assertRaises(ValueError, self.vim.set_mode, 'invalid-mode')

    def testSetModeSetter(self):
        self.vim.mode = 'insert'
        self.vim.send_keys('spam')
        self.vim.set_mode('normal')
        self.assertEqual(self.vim.display_lines()[0].strip(), 'spam')

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
