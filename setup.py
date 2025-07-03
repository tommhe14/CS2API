import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="cs2api",
    version="0.1.2",  
    description="Python API wrapper for Counter-Strike 2 professional match data via BO3.gg",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tommhe14/cs2api",
    author="tommhe14",
    author_email="theckley@yahoo.co.uk",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "aiohttp>=3.8.0",  
    ],
    python_requires=">=3.8",
    keywords="cs2 counter-strike esports api wrapper",
    project_urls={
        "Bug Reports": "https://github.com/tommhe14/cs2api/issues",
        "Source": "https://github.com/tommhe14/cs2api",
    },
)
