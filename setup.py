#!/usr/bin/env python

from setuptools import setup, find_packages
 
setup (
    name='bpmappers',
    version='0.2',
    description='Model to dictionary mapping for Python',
    author='K.K. BeProud',
    author_email='tokibito@gmail.com',
    url='http://www.beproud.jp/',
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
