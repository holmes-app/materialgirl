#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from materialgirl import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
]

setup(
    name='materialgirl',
    version=__version__,
    description='MaterialGirl is a library to keep materialized views and consolidations up-to-date.',
    long_description='''
MaterialGirl is a library to keep materialized views and consolidations up-to-date.
''',
    keywords='mysql database redis',
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    url='http://materialgirllib.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'redis',
        'msgpack-python',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
