.PHONY: docs

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
	docker compose stop
	docker compose -f docker-compose.yml -f docker-compose.local.yml build
	docker compose -f docker-compose.yml -f docker-compose.local.yml up

docker-deploy-dev:
	docker compose stop
	docker compose -f docker-compose.yml -f docker-compose.deploy.dev.yml build
	docker compose -f docker-compose.yml -f docker-compose.deploy.dev.yml up -d

graphql-schema:
	# assumes that you have docker running and a local setup for caster-editor
	docker compose -f docker-compose.yml -f docker-compose.local.yml exec backend ./generate_graphql_schema.sh
	cd caster-editor && yarn codegen
	@echo "Sucessfully generated new schema in caster-editor/graphql/graphql.ts"
