#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['-v', self.distribution.test_suite]
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


def read(path):
    with open(path) as f:
        return f.read()


setup(
    name='headlessvim',
    version='0.0.3',
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
    author='Ryosuke Ito',
    author_email='rito.0305@gmail.com',
    license='MIT',
    packages=['headlessvim'],
    install_requires=['pyte>=0.4.10', 'six>=1.9.0'],
    tests_require=['pytest', 'mock'],
    setup_requires=['flake8'],
    test_suite='tests',
    cmdclass={'test': PyTest},
)
