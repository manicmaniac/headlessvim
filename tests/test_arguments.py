#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from headlessvim.arguments import Parser


@pytest.fixture
def parser(request):
    return Parser('-N -i NONE -n -u NONE')


def test_parse(parser):
    assert parser.parse(None) == ['-N', '-i', 'NONE', '-n', '-u', 'NONE']
    args = ['-i', 'NONE', '-u', 'NONE']
    assert parser.parse('-i NONE -u NONE') == args
    assert parser.parse(args) == args


def test_default_args(parser):
    assert parser.default_args == '-N -i NONE -n -u NONE'
