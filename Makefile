.PHONY: docs

create-venv:
	python3 -m venv caster-back/venv && (\
		caster-back/venv/bin/activate;
		pip3 install -r caster-back/requirements-test.txt;
	)

docs:
	pip3 install --quiet -r requirements-docs.txt
	rm -rf docs/_build
	make -C docs html
ifeq ($(shell uname), Darwin)
	open docs/_build/html/index.html
endif

dev-server:
	. caster-back/venv/bin/activate && (\
		pip3 install --quiet -r requirements-docs.txt; \
		cd caster-back; \
		export SUPERCOLLIDER_HOST=localhost; \
		export SUPERCOLLIDER_PORT=57120; \
		python manage.py runserver --settings gencaster.settings.test; \
	)

docker-local:
	docker-compose stop
	docker-compose build
	docker-compose -f docker-compose.yml -f docker-compose.local.yml up

docker-prod:
	docker-compose stop
	docker-compose build
	docker-compose -f docker-compose.yml -f docker-compose.deploy.yml up -d
