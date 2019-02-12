from setuptools import setup, find_packages

setup(
    name="webcollector",
    version="0.0.3-alpha",
    author="Jun Hu",
    packages=find_packages(
        exclude=[
            'examples'
        ]
    ),
    install_requires=[
        "html5lib",
        "aiohttp",
        "BeautifulSoup4"
    ],
    description="WebCollector-Python is an open source web crawler framework based on Python.It provides some simple interfaces for crawling the Web,you can setup a multi-threaded web crawler in less than 5 minutes.",
    license="GNU General Public License v3.0 (See LICENSE)",
    url="https://github.com/CrawlScript/WebCollector-Python"
)