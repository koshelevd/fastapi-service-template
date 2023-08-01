SHELL := /bin/bash

clean: ## remove python/pytest cache files and other temp junk
	find . -name '*.pyc' | xargs rm -rf
	find . -name '*__pycache__' | xargs rm -rf
	find . -name '*.cache' | xargs rm -rf
	rm -r .pytest_cache 2>/dev/null || true

isort: ## sort imports
	isort .

black: ## format code
	black .

lint: clean isort black ## do autoflake, isort and black

run_db: ## run database
	docker-compose up -d

format: clean isort black ## do isort and black
