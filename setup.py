"""A package that enables open source workflows with the gSSURGO dataset."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gssurgo",
    version="0.0.5",
    author="Joseph Stachelek",
    author_email="stachel2@msu.edu",
    description="Python toolbox enabling an open source gSSURGO workflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jsta/gssurgo",
    scripts=["bin/extract_gssurgo_tif"],
    include_package_data=True,
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
