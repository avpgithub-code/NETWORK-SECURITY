from setuptools import setup, find_packages, Extension, setup
from typing import List
import os
import sys

HYPHEN_E_DOT = '-e .'
def read_requirements(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip() \
                and not line.startswith('#') and line.strip() != HYPHEN_E_DOT]
    except FileNotFoundError:
        return []

setup(
    name='network_security_tools',
    version='0.1.0',
    author='Archit Pandya',
    install_requires=read_requirements('REQUIREMENTS.TXT'),
    packages=find_packages(),
    # package_dir={'': 'src'},
    description='A collection of network security tools implemented in Python.',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)