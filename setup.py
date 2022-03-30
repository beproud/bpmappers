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
    version='1.3',
    description='bpmappers is a Python moudle that maps Python dictionary '
    'values and object properties to different dictionary.',
    long_description=read_file('README.rst'),
    long_description_content_type="text/x-rst",
    author='BeProud Inc.',
    author_email='tokibito@gmail.com',
    url='https://bpmappers.readthedocs.io/ja/stable/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['bpmappers'],
    keywords=['model', 'mapper', 'django'],
    license='MIT License',
    extras_require={
        'django': ['Django'],
        'develop': [
            'Django', 'pytest', 'flake8', 'pytest-django',
            'pytest-pythonpath', 'tox',
        ],
    },
)
