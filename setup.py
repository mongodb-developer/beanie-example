from setuptools import setup, find_packages

EXTRAS_REQUIRE = {
    "tests": [
        "pytest",
        "coverage[toml]>=5.0.2",
    ],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + [
    "ruff",
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
        "fastapi==0.114.0",
        "beanie==1.26.0",
        "pydantic == 2.9.1",
        "pydantic-settings==2.4.0",
        "motor==3.5.1",
        "tqdm==4.66.5",
        "uvicorn",
    ],
    extras_require=EXTRAS_REQUIRE,
    entry_points={
        "console_scripts": [
            "init-db=beaniecocktails.scripts.init_db:main",
        ],
    },
)
