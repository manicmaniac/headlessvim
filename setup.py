#!/usr/bin/env python
# -*- coding:utf-8 -*-

import platform
from setuptools import setup


def tests_require():
    res = []
    version = platform.python_version()
    if version < '2.7.0':
        res.append('unittest2')
    if version < '3.3.0':
        res.append('mock')
    return res


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
    install_requires=['pyte>=0.4.10'],
    tests_require=tests_require(),
    setup_requires=['flake8'],
    use_2to3=True,
    test_suite='tests',
)
