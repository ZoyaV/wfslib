#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages # type: ignore
from os import path

setup(
    name="WFSLib",
    version="1.0",
    package_data={'': ['*.*']},
    packages=find_packages(),
)
