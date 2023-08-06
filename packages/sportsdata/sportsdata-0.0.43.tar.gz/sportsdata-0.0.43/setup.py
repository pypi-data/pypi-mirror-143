from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sportsdata",
    version="0.0.43",
    author="David Orkin",
    author_email="david.orkin@fuzzybumblebee.org",
    description="A collection of sports apis and higher level abstraction classes (Games, Season, Player, League, etc)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://opensource.fuzzybumblebee.org/sportsdata",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
    package_dir={"": "src"},
    package_data={'sportsdata': ['data/*.json']},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['pandas']
)

