from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='botal',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        "requests",
        "vk_api"
    ],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
)
