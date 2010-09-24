# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='dbtc_exporter',
    version='1.0',
    description="Don't Break The Chain exporter",
    author='Tim Freund',
    author_email='tim@freunds.net',
    license = 'MIT License',
    url='http://github.com/timfreund/dbtc_exporter',
    install_requires=[
        'BeautifulSoup',
        'twill',
                ],
    packages=['dbtc_exporter'],
    include_package_data=True,
    entry_points="""
    [console_scripts]
    dbtcexporter = dbtc_exporter:execute
    """,
)
