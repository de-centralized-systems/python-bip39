from setuptools import setup
import pathlib


# Get the long description from the README file.
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text()

setup(
    name="bip39",
    version="0.0.2",
    author="Aljosha Judmayer and Philipp Schindler",
    author_email="ajudmayer@sba-research.org",
    description="A self-contained and simple BIP39 implementation in Python",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/de-centralized-systems/python-bip39/",
    extras_require={"dev": ["pytest"]},
    py_modules=["bip39"],
    scripts=["bip39.py"],
    classifiers=[
        "Development Status :: 4 - Beta",  # 5 - Production/Stable;
        "Environment :: Console",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
    project_urls={
        "Source": "https://github.com/de-centralized-systems/python-bip39/",
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    python_requires=">=3.6",
)
