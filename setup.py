from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="ethioqen",
    version="0.2.0",
    author="Beabfekad Zikie",
    author_email="beabzk@proton.me",
    description="A package for Ethiopian date and time conversions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beabzk/ethioqen",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Localization",
    ],
    python_requires=">=3.8",
    project_urls={
        "Bug Reports": "https://github.com/beabzk/ethioqen/issues",
        "Source": "https://github.com/beabzk/ethioqen",
    },
)