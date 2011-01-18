#!/usr/bin/env python
from distutils.core import setup
import sys

kwds = {}
kwds['long_description'] = open('README.txt').read()

if sys.version_info[:2] < (2, 6):
    raise Exception('This version of ga needs Python 2.7 or later. ')

setup(name='ga',
      version='0.1',
      description='Genetic Algorithm library',
      author='Valerie Hendrix',
      author_email='val.hendrix@me.com',
      url='https://github.com/valreee/GeneticAlgorithms',
      download_url='https://valreee@github.com/valreee/GeneticAlgorithms.git',
      license='',
      py_modules=['ga.goldberg','ga.utilities','ga.simple','ga.tsp','ga.common'],
      platforms='all',
      classifiers = [
        'Development Status :: .1 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      **kwds
      )

