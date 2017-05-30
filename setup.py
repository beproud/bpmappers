import os
from setuptools import setup


def read_file(filename):
    basepath = os.path.dirname(os.path.dirname(__file__))
    filepath = os.path.join(basepath, filename)
    if os.path.exists(filepath):
        return open(filepath).read()
    else:
        return ''


setup(
    name='bpmappers',
    version='0.9dev',
    description='A mapping tool from model to dictionary.',
    long_description=read_file('README.rst'),
    author='BeProud Inc.',
    author_email='tokibito@gmail.com',
    url='http://bpmappers.readthedocs.org/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['bpmappers'],
    keywords=['model', 'mapper', 'django'],
    license='MIT License',
    install_requires=['six'],
    extras_require={
        'django': ['Django'],
        'develop': [
            'Django', 'pytest', 'flake8', 'pytest-django',
            'pytest-pythonpath', 'tox',
        ],
    },
)
