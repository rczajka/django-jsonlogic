from setuptools import setup
from setuptools.command.test import test as TestCommand

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


class Tox(TestCommand):
    def run_tests(self):
        import sys
        import tox
        sys.exit(tox.cmdline())

setup(
    name='django-jsonlogic',
    version='0.1.1',
    description='Django form widget for editing logic in JSON-Logic format.',
    long_description=long_description,
    url='https://github.com/rczajka/django-jsonlogic',
    author='Radek Czajka',
    author_email='rcz-git@rczajka.pl',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='django json logic',
    packages=['jsonlogic_widget'],
    install_requires=[
        'Django>=1.8,<1.11',
        'json-logic>=0.7.0-alpha',
    ],
    extras_require={
        'test': ['tox'],
    },
    package_data={
        'jsonlogic_widget': ['static/jsonlogic/*', 'templates/jsonlogic/*'],
    },
    cmdclass={
        'test': Tox
    },
)
