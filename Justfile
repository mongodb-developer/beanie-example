run:
	python -m uvicorn --reload beaniecocktails:app 

check:
	python -m ruff check

clean:
	rm -rf build dist src/*.egg-info .tox .pytest_cache pip-wheel-metadata .DS_Store
	find src -name '__pycache__' | xargs rm -rf
	find tests -name '__pycache__' | xargs rm -rf

install:
	python -m pip install -e .

dev:
	python -m pip install -e .[dev]
