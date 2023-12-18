#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'PyYAML>=5.0']
# install_requires=['pandas>=1.0', 'scipy==1.1', 'matplotlib>=2.2.1,<3']

test_requirements = ['pytest>=3', ]

setup(
    author="Hasan-UL-Banna, Asadullah Al Galib",
    author_email='hasanulbanna04056@gmail.com, asadullahgalib13@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
    ],
    description="confiGOAT is a powerful, flexible, and developer-friendly configuration management tool.",
    entry_points={
        'console_scripts': [
            'configoat=configoat.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='configoat',
    name='configoat',
    packages=find_packages(include=['configoat', 'configoat.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/aag13/configoat',
    version='0.1.6',
    zip_safe=False,
)
