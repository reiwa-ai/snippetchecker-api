#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''

# version
here = os.path.dirname(os.path.abspath(__file__))
version = '0.1.0'

setup(
    name="snippetchecker-api",
    version=version,
    project_urls = {
    'homepage': 'https://www.reiwa-ai.co.jp/snippetbox.html',
    'repository': 'https://github.com/reiwa-ai/snippetchecker-api',
    'documentation': 'https://reiwa-ai.github.io/snippetchecker-api/',
    },
    author='Toshiyuki Sakamto',
    author_email='toshiyuki.sakamoto@reiwa-ai.co.jp',
    maintainer='Reiwa AI K.K.',
    maintainer_email='contact@reiwa-ai.biz',
    description='Check LLM generated snippets',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=['snippetchecker','snippetchecker.scripts'],
    install_requires=[],
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
    ],
)
