# -*- coding: utf-8 -*-
import re
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


here = os.path.dirname(os.path.abspath(__file__))
version_re = re.compile(r"__version__ = (\'.*?\')")
with open(os.path.join(os.path.join(here, 'sadisplay'), '__init__.py')) as f:
    version = None
    for line in f:
        match = version_re.search(line)
        if match:
            version = eval(match.group(1))
            break
    else:
        raise Exception("Cannot find version in sadisplay.py")


setup(
    name='sadisplay',
    version=version,
    url='http://bitbucket.org/estin/sadisplay',
    license='BSD',
    author='Evgeniy Tatarkin',
    author_email='tatarkin.evg@gmail.com',
    description='SqlAlchemy schema display script',
    long_description=open(os.path.join(here, 'README.rst')).read(),
    packages=['sadisplay', ],
    zip_safe=False,
    platforms='any',
    tests_require=['nose >= 1.0', ],
    test_suite='nose.collector',
    install_requires=[
        'SQLAlchemy >= 0.5',
    ],
    entry_points={
        'console_scripts': ['sadisplay = sadisplay.reflect:run', ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
