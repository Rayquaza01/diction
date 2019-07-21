#!/usr/bin/env python3
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="diction",
      version="1.0.1",
      description="A wordnik commandline client",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/Rayquaza01/diction",
      author="Rayquaza01",
      author_email="rayquaza01@outlook.com",
      license="MIT",
      scripts=["bin/diction.py"],
      include_package_data=True,
      package_data={"": ["README.md"]},
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent"
      ])
