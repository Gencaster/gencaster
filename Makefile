.PHONY: docs

DOCKER_EDITOR = -f docker-compose.editor.yml
DOCKER_FRONTEND = -f docker-compose.frontend.yml
DOCKER_LOCAL = -f docker-compose.yml -f docker-compose.local.yml
DOCKER_DEPLOY_DEV = -f docker-compose.yml -f docker-compose.deploy.dev.yml
DOCKER_DEPLOY_LIVE = -f docker-compose.yml -f docker-compose.deploy.live.yml
DOCKER_ALL_FILES = $(DOCKER_LOCAL) $(DOCKER_EDITOR) $(DOCKER_FRONTEND) -f docker-compose.deploy.dev.yml -f docker-compose.deploy.live.yml

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
		export SUPERCOLLIDER_HOST=127.0.0.1; \
		export SUPERCOLLIDER_PORT=57120; \
		python manage.py runserver --settings gencaster.settings.test; \
	)

docker-local:
	docker compose $(DOCKER_ALL_FILES) stop
	$(eval FILES += $(DOCKER_LOCAL))
ifdef no-editor
	@echo "Start with NO editor"
else
	$(eval FILES += $(DOCKER_EDITOR))
endif
ifdef no-frontend
	@echo "Start with NO frontend"
else
	$(eval FILES += $(DOCKER_FRONTEND))
endif
ifdef no-sound
	@echo "Start with NO sound container"
	$(eval ENV_VARIABLES += GENCASTER_SOUND_REPLICAS=0)
endif
	@echo "Start with $(FILES)"
	@echo "Start with env $(ENV_VARIABLES)"
	docker compose $(FILES) build
	$(ENV_VARIABLES) docker compose $(FILES) up

docker-deploy-dev:
	docker compose $(DOCKER_ALL_FILES) stop
	docker compose $(DOCKER_DEPLOY_DEV) build
	docker compose $(DOCKER_DEPLOY_DEV) up -d

docker-deploy-live:
	docker compose $(DOCKER_ALL_FILES) stop
	docker compose $(DOCKER_DEPLOY_LIVE) build
	docker compose $(DOCKER_DEPLOY_LIVE) up -d

docker-stop:
	docker compose $(DOCKER_ALL_FILES) stop

graphql-schema:
	# assumes that you have docker running and a local setup for caster-editor
	docker compose -f docker-compose.yml -f docker-compose.local.yml exec backend ./generate_graphql_schema.sh
	cd caster-editor && npm run codegen
	cd caster-front && npm run codegen
	@echo "Sucessfully generated new schema in caster-editor/src/graphql/graphql.ts"

test-backend: venv virtualenv
	. caster-back/venv/bin/activate && (\
		cd caster-back; \
		export DJANGO_SETTINGS_MODULE="gencaster.settings.dev_local"; \
		./run_tests.sh; \
	)

test-editor:
	# node is not nice in regards of pid, see
	# https://stackoverflow.com/a/59234367/3475778
	# sending it to background with & and kill the pid does not work!
	# therefore we kill every node process :)
	cd caster-editor && (\
		npm run type-check && \
		(npm run dev&) && \
		npm run cypress:run && \
		pkill -9 node \
	)

test-frontend:
	cd caster-front && (\
		npm run type-check \
	)

test: test-backend test-editor test-frontend
