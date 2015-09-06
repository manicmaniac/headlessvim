#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest

from headlessvim.arguments import Parser


@pytest.fixture
def default_args(request):
    return ['-N', '-i', 'NONE', '-n', '-u', 'NONE']


@pytest.fixture
def parser(request, default_args):
    return Parser(default_args)


@pytest.fixture
def args(request):
    return ['-i', 'NONE', '-u', 'NONE']


def test_parse(parser, default_args, args):
    assert parser.parse(None) == default_args
    assert parser.parse('-i NONE -u NONE') == args
    assert parser.parse(args) == args


def test_default_args(parser, default_args):
    assert parser.default_args == default_args
