# -*- coding: utf-8 -*-
#
#   Copyright [2011] [Patrick Ancillotti]
#   Copyright [2011] [Jason Kölker]
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()
HISTORY = open(os.path.join(here, "HISTORY.rst")).read()

install_requires = [
    'requests',
    'anyjson'
]

classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python",
]


setup(
    name='daikon',
    version='1.50',
    description='ElasticSearch CLI',
    long_description="\n" + README + "\n\n" + HISTORY,
    classifiers=classifiers,
    keywords='',
    author='Patrick Ancillotti',
    author_email='patrick@eefy.net',
    url='http://www.github.com/neogenix/daikon',
    license='LICENSE',
    packages=find_packages(
        exclude=[
            'ez_setup',
            'examples',
            'tests'
        ]
    ),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    data_files=[
        ('/etc/daikon', ['daikon.conf'])
    ],
    entry_points={
        'console_scripts': ['daikon = daikon:main']
    },
)
