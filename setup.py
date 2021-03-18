from setuptools import setup, find_packages

EXTRAS_REQUIRE = {
    "tests": [
        "pytest",
        "coverage[toml]>=5.0.2",
    ],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + [
    "black",
    "twine",
    "wheel",
    "prospector[with_everything]",
]

setup(
    name="beanie-cocktails",
    description="A cocktail API built with MongoDB and Beanie",
    version="0.0.0",
    author="Mark Smith",
    author_email="mark.smith@mongodb.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi==0.63.0",
        "beanie==0.2.3",
        "uvicorn[standard] == 0.12.2",
        "dnspython",
    ],
    extras_require=EXTRAS_REQUIRE,
)