from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="runtime-environment-capture",
    version="0.2.0",
    author="Carson Woods",
    description="A wrapper to collect data for ensuring reproducibility.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carsonwoods/rec",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "rec=rec.__main__:main",
        ]
    },

)
