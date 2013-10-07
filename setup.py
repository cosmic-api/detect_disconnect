#!/usr/bin/python

from setuptools import setup

with open("README.md") as readme:
    long_description = readme.read()

setup(
    name = 'detect_disconnect',
    version = "0.0.1",
    url = "https://github.com/cosmic-api/detect_disconnect",
    description = 'A high-level web API framework',
    license = "MIT",
    author = "8313547 Canada Inc.",
    author_email = "kyu.lee@cosmic-api.com",
    long_description = long_description,
    install_requires = [
        "cosmic==0.0.7"
    ]
)
