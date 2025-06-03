from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="opet",
    author="Sinan Erdinc",
    author_email="hello@sinanerdinc.com",
    version="0.1.0",
    install_requires=["requests", "click"],
    description="A Python package that allows you to view fuel prices in Turkey based on cities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sinanerdinc/opet",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'opet-cli=opet.main:cli',
        ],
    },
    packages=find_packages(),
    package_dir={'opet': 'opet'},
    python_requires=">=3.0"
)
