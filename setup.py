#!/usr/bin/env python
# -*- coding:utf-8 -*-

try:
    from setuptools import setup
    from setuptools.command.test import test as TestCommand
except ImportError:
    from distutils import setup
else:
    class PyTest(TestCommand):
        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = ['-v', 'tests']
            self.test_suite = True

        def run_tests(self):
            import sys
            import pytest
            sys.exit(pytest.main(self.test_args))


setup(name='headlessvim',
      version='0.0.1',
      description='',
      author='Ryosuke Ito',
      author_email='rito.0305@gmail.com',
      license='MIT',
      packages=['headlessvim'],
      install_requires=['pyte>=0.4.10'],
      setup_requires=['flake8'],
      cmdclass={'test': PyTest})
