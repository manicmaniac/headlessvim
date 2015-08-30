#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup


setup(
    name='headlessvim',
    version='0.0.2',
    description='programmable Vim, no need of +clientserver!',
    long_description=open('README.rst').read(),
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
    tests_require=['mock'],
    use_2to3=True,
    test_suite='tests',
)
