from setuptools import find_packages
from setuptools import setup

setup(
    name='com_pub',
    version='0.0.0',
    packages=find_packages(
        include=('com_pub', 'com_pub.*')),
)
