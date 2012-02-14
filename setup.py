import os
from setuptools import setup, find_packages

def read_file(filename):
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
    if os.path.exists(filepath):
        return open(filepath).read()
    else:
        return ''


setup(
    name='bpmappers',
    version='0.5.1',
    description='Model to dictionary mapping for Python',
    long_description=read_file('README.txt'),
    author='K.K. BeProud',
    author_email='shinya.okano@beproud.jp',
    url='http://tokibito.bitbucket.org/bpmappers/',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Plugins',
      'Framework :: Django',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.5',
      'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    keywords=['model', 'mapper', 'django'],
    license='BSD License',
    test_suite='tests',
)
