import os

__package_name__ = "despace"
__author__ = "Ruibin Liu"

from setuptools import setup, find_packages

if os.path.exists('README.md'):
    long_description = open('README.md').read()
else:
    long_description = 'Despace - A python package to sort or index N-dimensional data without using space filling curves.'

with open('requirements.txt') as f:
    REQUIREMENTS = f.read().strip().split('\n')

with open('despace/version.py', 'r') as vf:
    __version__ = vf.readline().split()[-1].strip().replace("'", '')


setup(
    name=__package_name__,
    version=__version__,
    author=__author__,
    author_email="ruibinliuphd@gmail.com",
    description="A spatial decomposition tool for sorting or indexing N-D data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruibin-Liu/despace",
    project_urls={
        "Bug Tracker": "https://github.com/Ruibin-Liu/despace/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    python_requires=">=3.6",
)
