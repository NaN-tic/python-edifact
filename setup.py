# encoding: utf8
##############################################################################
#
#    Copyright (C) 2011-2018 NaN Projectes de Programari Lliure, S.L.
#                            http://www.NaN-tic.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from setuptools import setup, find_packages
import os
import sys
from edifact.version import VERSION, LICENSE, WEBSITE


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if sys.version_info < (3, 0):
    install_requires = ['enum34', 'future']
else:
    install_requires = []

setup(
    name='edifact',
    version=VERSION,
    author='NaN-tic',
    author_email='developers@nan-tic.com',
    description='Python EDI file parser.',
    long_description=read('README'),
    url=WEBSITE,
    download_url='https://bitbucket.org/nantic/python-edifact/',
    packages=find_packages(),
    package_data={
        'tests': ['data/*'],
        },
    install_requires=install_requires,
    use_2to3=True,
    license=LICENSE,
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 '
        'or later (LGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
)
