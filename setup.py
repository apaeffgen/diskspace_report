#!/usr/bin/python3
import os
from setuptools import setup, find_packages

root = os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))
os.chdir(root)

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='diskspace_report',
    version='0.3.0',
    author='Andreas Paeffgen',
    author_email='opensource@software-geeks.de',
    description='Check the available disk space and write it to a csv file. Eventually email the csv file.',
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/apaeffgen/diskspace_report',
    packages=find_packages(),
    license="Apache License 2.0",
    install_requires=[
        'pylocale>=0.0.1',
        'click>=7.1.2',
    ],


    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        "console_scripts" : [
            "diskspace_report = diskspace_report:main",
        ],
    },
    python_requires='>=3.6',
)
