pwd=$(shell pwd)
SHELL=/bin/bash -o errexit -o pipefail -o nounset

build:
	@docker-compose build --pull

run: build
	@docker-compose up

migrations_check: run
	@echo "Migration check..."
	@docker-compose exec -T app \
		./manage.py makemigrations --dry-run | grep -q "No changes detected"

migrations:
	@echo "Make migrations..."
	@docker-compose exec -T app \
		./manage.py makemigrations

migrate:
	@docker-compose exec app ./manage.py migrate

frozen_requirements:
	@python3 -m venv .tmpvenv
	@.tmpvenv/bin/pip install -U pip setuptools
	@.tmpvenv/bin/pip install --no-cache-dir --requirement app/requirements.txt
	@.tmpvenv/bin/pip freeze | grep -v "pkg-resources" > app/requirements.frozen.txt
	@rm -rf .tmpvenv
	@docker-compose build --pull app