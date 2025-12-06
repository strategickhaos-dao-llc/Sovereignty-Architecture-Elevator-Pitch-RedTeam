#!/usr/bin/env python3
"""
FlameLang Setup Script
pip installable package
"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flamelang',
    version='0.1.0',
    description='Sovereign Programming Language with Physics Integration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Strategickhaos DAO LLC',
    author_email='contact@strategickhaos.com',
    url='https://github.com/Strategickhaos/flamelang',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.20.0',
        'sympy>=1.9',
        'scipy>=1.7.0',
        'psutil>=5.8.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'black>=21.0',
            'flake8>=3.9',
        ],
    },
    entry_points={
        'console_scripts': [
            'flamelang=core.repl:start_repl',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Compilers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    keywords='compiler physics sovereign programming-language',
    project_urls={
        'Bug Reports': 'https://github.com/Strategickhaos/flamelang/issues',
        'Source': 'https://github.com/Strategickhaos/flamelang',
    },
)
