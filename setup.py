#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys




class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['konoha/tests', '-s']
        self.test_suite = True

    def run_tests(self):
        import pytest
        # os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='konoha',
    version='2.0',
    author='mturilin',
    author_email='mikhail@turilin.com',
    description='CMS for Django',
    license='MIT',
    url='https://github.com/mturilin/konoha',
    packages=['konoha'],
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'Django',
        'PyYAML',
        'Coffin',
        'django-treeadmin',
        'jinja2',
        'django-filer',
        'funcy',
        'Markdown',
        'django-tools',

    ],
    tests_require=[
        'pytest',
        'pytest-django',
        'Django',
        'beautifulsoup4',
        'path.py',
    ],
      dependency_links=[
        'git+https://github.com/mturilin/import_helpers',
    ],
    cmdclass={'test': PyTest},
)
