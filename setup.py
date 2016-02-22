#!/usr/bin/env python

import os

from setuptools import setup, find_packages

if os.environ.get('USER', '') == 'vagrant':
  del os.link


setup(
  name='monica',
  version='0.0.2',
  description='monica helps you order food from the commandline',
  long_description=open('README.rst').read(),
  author='Gyanendra Mishra',
  author_email='anomaly.the@gmail.com',
  license='MIT',
  keywords=['license', 'food', 'monica', 'command line', 'cli', 'zomato'],
  url='https://github.com/zephrys/monica',
  packages=find_packages(exclude=['contrib', 'docs', 'tests']),
  install_requires=[
    'docopt>=0.6.2',
    'requests>=2.8.0',
    'tabulate==0.7.5'
  ],
  entry_points={
    'console_scripts': [
        'monica = monica.monica:main'
    ],
  }
)