import os
from setuptools import setup, find_packages

from SFDjangoUtils import VERSION

setup(
    name='SFDjangoUtils',
    version=".".join(map(str, VERSION)),
    description='SFDjangoUtils',
    long_description="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
)
