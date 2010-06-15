#!/usr/bin/env python
#:coding=utf-8:

from setuptools import setup, find_packages
 
setup (
    name='bpmappers',
    version='0.1',
    description='Model to dictionary mapping for Python',
    author='K.K. BeProud',
    author_email='tokibito@gmail.com',
    url='https://www.beproud.jp/',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Plugins',
      'Framework :: Django',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=["bpmappers"],
    test_suite='tests',
)
