from os import getenv
from setuptools import setup
from setuptools import find_packages


setup(
    name='tennis-point-parser',
    version=getenv("VERSION", "LOCAL"),
    description='Parses tennis points',
    packages=find_packages()
)
