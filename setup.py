#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
    name='Diskspace_Report',
    version='0.1.1',
    author='Andreas Paeffgen',
    author_email='your.email@example.com',
    description='Check the available disk space and write it to a csv file. Eventually email the csv file.',
    url='https://github.com/apaeffgen/diskspace_report',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
