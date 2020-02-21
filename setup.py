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
along with Fangfrisch. If not, see <https://www.gnu.org/licenses/>.
"""
import setuptools

import fangfrisch

source_url = 'https://github.com/rseichter/fangfrisch'
with open('README.rst', 'r') as f:
    long_description = f.read()
setuptools.setup(
    name='fangfrisch',
    version=fangfrisch.__version__,
    packages=[
        'fangfrisch',
        'fangfrisch.config',
    ],
    entry_points={
        'console_scripts': ['fangfrisch = fangfrisch.__main__:main'],
    },
    url=source_url,
    project_urls={
        'Documentation': 'https://rseichter.github.io/fangfrisch/',
        'Source': f'{source_url}',
        'Tracker': f'{source_url}/issues',
    },
    license='GPLv3+',
    author='Ralph Seichter',
    author_email='fangfrisch@seichter.de',
    description='Update and verify unofficial Clam Anti-Virus signatures',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords='antivirus clamav freshclam refresh update',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests >= 2.22.0',
        'SQLAlchemy >= 1.3.13',
    ],
    python_requires='>=3.7',
)
