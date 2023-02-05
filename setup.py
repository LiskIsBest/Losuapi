from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

VERSION = "0.0.1"

setup(
    name="losuapi",
    version=VERSION,
    description="Python wrapper for the Osu apiv2.",
    long_description=long_description,
    keywords=["python","osu","api","wrapper"],
    author="Darien Moore",
    author_email="LiskIsBest@gmail.com",
    url="https://github.com/LiskIsBest/Losuapi",
    download_url="https://github.com/LiskIsBest/Losuapi/tarball/main",
    license="GPLv3",
    packages=find_packages(),
)