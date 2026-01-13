import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='goto-statement',
    version='2.0',
    url='https://github.com/heipa24/python-goto/',
    description='A function decorator that rewrites the bytecode, '
                'enabling goto in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['goto'],
    python_requires='>=3.6',
    author='Sebastian Noack',
    author_email='sebastian.noack@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
