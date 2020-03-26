#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dualmesh",
    version="0.14.0",
    author="Bartosz Bartmanski",
    author_email="bartoszbartmanski@gmail.com",
    description="Python module for generating dual meshes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BartoszBartmanski/DualMesh",
    python_requires='>=3.6',
    install_requires=[
        "meshio",
        "numpy"
    ],
    packages=setuptools.find_packages(),
)
