.PHONY: docs

DOCKER_LOCAL_NO_EDITOR = -f docker-compose.yml -f docker-compose.local.yml
DOCKER_LOCAL = $(DOCKER_LOCAL_NO_EDITOR) -f docker-compose.local.editor.yml
DOCKER_DEPLOY_DEV = -f docker-compose.yml -f docker-compose.deploy.dev.yml
DOCKER_ALL_FILES = $(DOCKER_LOCAL) -f docker-compose.deploy.dev.yml

venv: caster-back/venv/touchfile

.PHONY: virtualenv
virtualenv:
	pip3 install virtualenv

caster-back/venv/touchfile: requirements-docs.txt
	test -d caster-back/venv || virtualenv caster-back/venv
	. caster-back/venv/bin/activate; pip install -Ur requirements-docs.txt
	touch caster-back/venv/touchfile

docs: venv virtualenv
	rm -rf docs/_build
	. caster-back/venv/bin/activate; make -C docs html
ifeq ($(shell uname), Darwin)
	open docs/_build/html/index.html
endif

dev-server: venv virtualenv
	. caster-back/venv/bin/activate && (\
		pip3 install --quiet -r requirements-docs.txt; \
		cd caster-back; \
		export SUPERCOLLIDER_HOST=localhost; \
		export SUPERCOLLIDER_PORT=57120; \
		python manage.py runserver --settings gencaster.settings.test; \
	)

docker-local:
	docker compose $(DOCKER_ALL_FILES) stop
ifneq (,$(findstring e, $(MAKEFLAGS)))
	@echo "Start with NO editor"
	docker compose $(DOCKER_LOCAL_NO_EDITOR) build
	docker compose $(DOCKER_LOCAL_NO_EDITOR) up
else
	docker compose $(DOCKER_LOCAL) build
	docker compose $(DOCKER_LOCAL) up
endif

docker-deploy-dev:
	docker compose $(DOCKER_ALL_FILES) stop
	docker compose $(DOCKER_DEPLOY_DEV) build
	docker compose $(DOCKER_DEPLOY_DEV) up -d

graphql-schema: venv
	cd caster-back; . venv/bin/activate; python manage.py export_schema "gencaster.schema" > "schema.gql"
