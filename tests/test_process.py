#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import os
import time
from headlessvim.process import Process


class TestProcess(unittest.TestCase):
    def setUp(self):
        env = dict(os.environ, LANG='C')
        self.process = Process('vim', '-N -i NONE -n -u NONE', env)
        self.skip_terminate = False

    def tearDown(self):
        if not self.skip_terminate:
            self.process.terminate()

    def testTerminate(self):
        self.skip_terminate = True
        self.assertTrue(self.process.is_alive())
        self.process.terminate()
        self.assertFalse(self.process.is_alive())

    def testKill(self):
        self.skip_terminate = True
        self.assertTrue(self.process.is_alive())
        self.process.kill()
        self.assertFalse(self.process.is_alive())

    def testCheckReadable(self):
        time.sleep(0.5)
        self.assertTrue(self.process.check_readable(0.1))
        self.process.stdout.read()
        self.assertFalse(self.process.check_readable(0.1))

    def testExecutable(self):
        self.assertTrue('vim' in self.process.executable)
        self.assertTrue(os.path.isabs(self.process.executable))

    def testArgs(self):
        self.assertEqual(self.process.args, '-N -i NONE -n -u NONE')

    def test_stdin(self):
        self.assertTrue(hasattr(self.process.stdin, 'read'))

    def test_stdout(self):
        self.assertTrue(hasattr(self.process.stdin, 'write'))
