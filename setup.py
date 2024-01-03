#!/usr/bin/python3
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='Diskspace-Report',
    version='0.1.9',
    author='Andreas Paeffgen',
    author_email='your.email@example.com',
    description='Check the available disk space and write it to a csv file. Eventually email the csv file.',
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/apaeffgen/diskspace_report',
    packages=find_packages(),
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
