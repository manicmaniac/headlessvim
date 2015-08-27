#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from headlessvim.arguments import Parser


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser('-N -i NONE -n -u NONE')

    def testParse(self):
        expect = ['-N', '-i', 'NONE', '-n', '-u', 'NONE']
        self.assertEqual(self.parser.parse(None), expect)
        args = ['-i', 'NONE', '-u', 'NONE']
        self.assertEqual(self.parser.parse('-i NONE -u NONE'), args)
        self.assertEqual(self.parser.parse(args), args)

    def testDefaultArgs(self):
        expect = '-N -i NONE -n -u NONE'
        self.assertEqual(self.parser.default_args, expect)
