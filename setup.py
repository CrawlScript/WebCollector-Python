from setuptools import setup, find_packages

setup(
    name="webcollector",
    version="0.0.1-alpha",
    author="Jun Hu",
    packages=find_packages(
        exclude=[
            'examples'
        ]
    ),
    install_requires=[
        "aiohttp",
        "BeautifulSoup4"
    ],
    description="""
        An open source web crawler framework.
    """,
    license="GNU General Public License v3.0 (See LICENSE)",
    url="https://github.com/CrawlScript/WebCollector-Python"
)