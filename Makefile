install:
	poetry install

reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

build:
	poetry build

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest