from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="PHONE COMPARER",
    version="0.1",
    author="Daniel_Wu",
    packages=find_packages(),
    install_requires = requirements,
)