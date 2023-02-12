from setuptools import find_packages, setup

with open("README.md", "r") as readme:
    long_description = readme.read()

VERSION = "0.0.7"

setup(
    name="losuapi",
    version=VERSION,
    description="Python wrapper for the Osu apiv2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["python","osu","api","wrapper"],
    author="Darien Moore",
    author_email="LiskIsBest@gmail.com",
    url="https://github.com/LiskIsBest/Losuapi/tree/v"+VERSION,
    download_url="https://github.com/LiskIsBest/Losuapi/tarball/v"+VERSION,
    license="GPLv3",
    packages=find_packages(),
    install_requires=[
		"httpx",
        "pydantic"
	]
)