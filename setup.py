# Copyright (C) 2017-2019 by Vd.
# This file is part of Periodic package.
# Periodic is released under the MIT License (see LICENSE).

from distutils.core import setup
from os.path import join, dirname

import periodic

setup(
    name='py-enigma',
    version=periodic.version,
    author='Vd',
    author_email='vd@vd2.org',
    url='https://github.com/vd2org/periodic',
    license='MIT',
    description='Simple tool for run asyncio tasks periodically.',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    packages=['periodic'],
    package_data=dict(periodic=['periodic/*.py',]),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
