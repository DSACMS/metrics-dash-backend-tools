from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="metrics-dash-backend-tools",
    version="0.1.1",
    author="Isaac Milarsky",
    author_email="isaac.milarsky@hhs.cms.gov",
    description="Backend tools for the DSACMS OSPO metrics dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
        "pygals"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)