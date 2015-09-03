#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os.path
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

sys.path.insert(0, os.path.abspath('headlessvim'))
from _version import * # flake8: noqa
sys.path.pop(0)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


def read(path):
    with open(path) as f:
        return f.read()


setup(
    name='headlessvim',
    version=__version__,
    description='programmable Vim, no need of +clientserver!',
    long_description=read('README.rst'),
    keywords='vim test',
    url='https://github.com/manicmaniac/headlessvim',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
    ],
    author=__author__,
    author_email=__email__,
    license='MIT',
    packages=['headlessvim'],
    install_requires=read('requirements.txt').splitlines(),
    tests_require=['pytest', 'mock'],
    cmdclass={'test': PyTest},
)
