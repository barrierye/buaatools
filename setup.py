#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0
import re
from setuptools import setup, find_packages

with open('buaatools/version.py') as f:
    exec(f.read())

setup(
    name = 'buaatools',
    version = __version__,
    description = 'Python library for BUAA tools',
    url = 'https://github.com/barrierye/BUAA-Tools',
    keywords = 'buaa buaatools',
    
    author = 'barriery',
    author_email = 'barriery@qq.com',
    maintainer = 'barriery',
    maintainer_email = 'barriery@qq.com',

    include_package_data=True,

    python_requires='>=3.5',

    install_requires=[
        'pytz==2019.2',
        'icalendar==4.0.3',
        'requests==2.22.0',
    ],

    packages = find_packages(where='.'),
)
