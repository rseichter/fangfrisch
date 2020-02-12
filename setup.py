"""
Copyright © 2020 Ralph Seichter

This file is part of "Fangfrisch".

Fangfrisch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Fangfrisch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar. If not, see <https://www.gnu.org/licenses/>.
"""
from setuptools import setup

from fangfrisch import VERSION

setup(
    name='fangfrisch',
    version=VERSION,
    packages=[
        'fangfrisch',
        'fangfrisch.config'
    ],
    url='https://seichter.de/',
    license='GPLv3+',
    author='Ralph Seichter',
    author_email='fangfrisch@seichter.de',
    description='Sibling to Clam Anti-Virus freshclam utility',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'requests >= 2.22.0',
        'SQLAlchemy >= 1.3.13'
    ],
    python_requires='>=3.7'
)
